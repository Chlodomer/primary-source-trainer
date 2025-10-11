"""
Classification and grading logic based on mediation depth algorithm.
Implements the shortest-path logic from the PRD.
"""

from typing import Dict, Set, List, Tuple
from collections import deque
from models import Scenario, SourceNode, Topic, Classification, GradingResult


def build_graph(scenario: Scenario) -> Dict[str, List[str]]:
    """
    Build adjacency list from edges.
    Returns dict mapping node_id -> list of connected node_ids.
    """
    graph = {}

    # Initialize all nodes including event and actual nodes
    all_ids = {scenario.event.id} | {node.id for node in scenario.nodes}

    # Also collect any node IDs mentioned in edges (for ghost/lost nodes)
    for edge in scenario.edges:
        all_ids.add(edge.from_id)
        all_ids.add(edge.to)

    for node_id in all_ids:
        graph[node_id] = []

    # Add edges
    for edge in scenario.edges:
        graph[edge.from_id].append(edge.to)

    return graph


def shortest_path_steps(graph: Dict[str, List[str]], start: str, end: str) -> int:
    """
    BFS to find shortest path length from start to end.
    Returns number of steps, or infinity if unreachable.
    """
    if start == end:
        return 0

    visited = {start}
    queue = deque([(start, 0)])

    while queue:
        current, depth = queue.popleft()

        for neighbor in graph.get(current, []):
            if neighbor == end:
                return depth + 1

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, depth + 1))

    return float('inf')


def classify_sources(scenario: Scenario, topic: Topic) -> Tuple[Set[str], Set[str]]:
    """
    Classify all extant nodes as primary or secondary for given topic.

    A source is PRIMARY if it is the closest EXTANT source along its transmission path.
    A source is SECONDARY if other EXTANT sources are closer to the topic anchor.

    Returns:
        (primary_node_ids, secondary_node_ids)
    """
    graph = build_graph(scenario)

    # Get only extant nodes
    extant_nodes = [node for node in scenario.nodes if node.extant]

    if not extant_nodes:
        return set(), set()

    # For each extant node, check if there's a CLOSER EXTANT node along any path from the anchor
    primary = set()
    secondary = set()

    for node in extant_nodes:
        depth_to_node = shortest_path_steps(graph, topic.anchor, node.id)

        if depth_to_node == float('inf'):
            continue  # Unreachable

        # Check if there's any other extant node that's closer to the anchor
        # AND lies on a path from anchor to this node
        is_closest_extant = True

        for other_node in extant_nodes:
            if other_node.id == node.id:
                continue

            depth_to_other = shortest_path_steps(graph, topic.anchor, other_node.id)
            depth_other_to_node = shortest_path_steps(graph, other_node.id, node.id)

            # If other_node is on the path from anchor to node AND is closer to anchor
            # then node is NOT the closest extant
            if (depth_to_other < depth_to_node and
                depth_to_other + depth_other_to_node == depth_to_node):
                is_closest_extant = False
                break

        if is_closest_extant:
            primary.add(node.id)
        else:
            secondary.add(node.id)

    return primary, secondary


def grade_submission(
    scenario: Scenario,
    topic: Topic,
    classifications: List[Classification]
) -> Tuple[int, int, List[GradingResult]]:
    """
    Grade student's classifications.

    Returns:
        (score, max_score, grading_results)
    """
    # Get correct answers
    primary_ids, secondary_ids = classify_sources(scenario, topic)

    # Create lookup for student answers
    student_answers = {c.node_id: c for c in classifications}

    results = []
    score = 0
    max_score = 0

    # Grade each extant node
    extant_nodes = [node for node in scenario.nodes if node.extant]

    for node in extant_nodes:
        student_class = student_answers.get(node.id)

        # Determine correct answer
        if node.id in primary_ids:
            correct = "primary"
        elif node.id in secondary_ids:
            correct = "secondary"
        else:
            correct = "unknown"

        # Check if student answered
        if not student_class:
            results.append(GradingResult(
                node_id=node.id,
                student_answer="no_answer",
                correct_answer=correct,
                is_correct=False,
                points=0,
                feedback="No classification provided."
            ))
            max_score += 3  # 1 for classification + 2 for justification
            continue

        # Grade classification
        student_ans = student_class.classification

        # Handle "dependent_on_topic" - check if topic actually changes classification
        if student_ans == "dependent_on_topic":
            # Check if this node changes between topics
            is_dependent = len(scenario.topics) > 1 and _node_changes_with_topic(scenario, node.id)
            if is_dependent:
                is_correct = True
                node_points = 2  # Bonus for recognizing topic dependency
                feedback = "Correct! This source's classification depends on the research question."
            else:
                is_correct = False
                node_points = 0
                feedback = f"Incorrect. This source is consistently {correct} regardless of topic."
        else:
            is_correct = (student_ans == correct)
            node_points = 1 if is_correct else 0

            if is_correct:
                # Provide detailed feedback about WHY it's primary/secondary
                node_obj = next((n for n in scenario.nodes if n.id == node.id), None)
                if correct == "primary":
                    if node_obj and len(node_obj.transmission) > 0:
                        lost_sources = ", ".join([t.via for t in node_obj.transmission])
                        feedback = f"Correct! This is PRIMARY - it's the closest extant source (based on lost sources: {lost_sources})."
                    else:
                        feedback = f"Correct! This is PRIMARY - it's the closest extant source to the event."
                else:
                    feedback = f"Correct! This is SECONDARY - other extant sources are closer to the event."
            else:
                feedback = f"Incorrect. This is a {correct} source, not {student_ans}."

        # Grade justification based on semantic correctness
        justification = student_class.justification
        justification_points = 0
        justification_feedback = ""

        if justification and is_correct:
            # Evaluate if the justification matches the node's actual characteristics
            graph = build_graph(scenario)
            depth = shortest_path_steps(graph, topic.anchor, node.id)

            # Determine what makes this source primary or secondary
            is_primary = node.id in primary_ids

            # Check if justification is semantically correct
            j_lower = justification.lower()

            if is_primary:
                # For primary sources, good justifications mention:
                # - Witness/contemporary/closest
                # - Timing (at the time, shortly after)
                # - Based on lost sources (making this the closest extant)
                if "witness" in j_lower and depth == 1:
                    justification_points = 2
                    justification_feedback = " ✓ Excellent reasoning - this is indeed an eyewitness account!"
                elif "closest" in j_lower or "surviving" in j_lower:
                    justification_points = 2
                    justification_feedback = " ✓ Excellent - correctly identified as the closest extant source!"
                elif ("earlier sources" in j_lower or "no longer exist" in j_lower) and "closest extant" in j_lower:
                    justification_points = 2
                    justification_feedback = " ✓ Perfect! This depends on lost sources, making it the closest extant source!"
                elif ("time of" in j_lower or "shortly after" in j_lower) and node.year <= scenario.event.year + 10:
                    justification_points = 2
                    justification_feedback = " ✓ Correct - the timing makes this primary!"
                else:
                    justification_points = 1
                    justification_feedback = " Justification is reasonable but could be more specific about why this is the *closest extant* source."

            else:  # Secondary source
                # For secondary sources, good justifications mention:
                # - Written long after (but OTHER extant sources are closer)
                # - Summarizes/analyzes OTHER EXTANT sources
                # - Modern scholarship
                # - Multiple steps removed
                if "long after" in j_lower and (node.year - scenario.event.year) > 50:
                    justification_points = 2
                    justification_feedback = f" ✓ Excellent - written {node.year - scenario.event.year} years after the event, and other extant sources are closer!"
                elif "modern scholarship" in j_lower or "modern" in j_lower and "analyz" in j_lower:
                    justification_points = 2
                    justification_feedback = " ✓ Correct - modern scholarship analyzing other surviving sources!"
                elif ("summarizes" in j_lower or "analyzes" in j_lower or "compiles" in j_lower or "synthesizes" in j_lower) and ("surviving" in j_lower or "extant" in j_lower or "earlier" in j_lower):
                    justification_points = 2
                    justification_feedback = " ✓ Correct - this analyzes/compiles other surviving sources!"
                elif "multiple steps" in j_lower or "several" in j_lower or "removed from" in j_lower or "transmission steps" in j_lower:
                    justification_points = 2
                    justification_feedback = " ✓ Good reasoning about mediation depth!"
                else:
                    justification_points = 1
                    justification_feedback = " Justification is reasonable but could be more specific about why other extant sources are closer to the event."

        elif justification and not is_correct:
            justification_feedback = " Your reasoning doesn't match this source's actual relationship to the event."

        feedback += justification_feedback

        total_points = node_points + justification_points
        score += total_points
        max_score += 3  # 1 for classification + 2 for justification

        results.append(GradingResult(
            node_id=node.id,
            student_answer=student_ans,
            correct_answer=correct,
            is_correct=is_correct,
            points=total_points,
            feedback=feedback
        ))

    return score, max_score, results


def _node_changes_with_topic(scenario: Scenario, node_id: str) -> bool:
    """
    Check if a node's classification changes between different topics.
    Used to validate "dependent_on_topic" answers.
    """
    if len(scenario.topics) < 2:
        return False

    classifications = []
    for topic in scenario.topics:
        primary, secondary = classify_sources(scenario, topic)
        if node_id in primary:
            classifications.append("primary")
        elif node_id in secondary:
            classifications.append("secondary")

    # If not all the same, it changes with topic
    return len(set(classifications)) > 1


def get_node_feedback(scenario: Scenario, node_id: str, topic: Topic) -> str:
    """
    Generate detailed feedback explaining why a node is primary/secondary.
    """
    node = next((n for n in scenario.nodes if n.id == node_id), None)
    if not node:
        return "Node not found."

    if not node.extant:
        return f"'{node.title}' is lost and therefore cannot be a primary source."

    graph = build_graph(scenario)
    depth = shortest_path_steps(graph, topic.anchor, node_id)

    primary_ids, _ = classify_sources(scenario, topic)
    is_primary = node_id in primary_ids

    feedback = f"**{node.title}** ({node.year} CE)\n\n"

    if depth == float('inf'):
        feedback += "This source has no documented connection to the event in question."
    elif depth == 0:
        feedback += "This is the event/anchor itself."
    elif is_primary:
        feedback += f"**Primary source** for this topic.\n"
        feedback += f"- Mediation depth: {depth} step(s) from {topic.label}\n"
        feedback += f"- Author role: {node.author_role}\n"

        if node.transmission:
            feedback += f"- Transmission: via {len(node.transmission)} intermediary step(s)\n"
        else:
            feedback += f"- Direct relationship to the event\n"

        feedback += f"\nThis is the closest extant source to the topic anchor."
    else:
        feedback += f"**Secondary source** for this topic.\n"
        feedback += f"- Mediation depth: {depth} step(s) from {topic.label}\n"
        feedback += f"- Author role: {node.author_role}\n"

        if node.transmission:
            trans_info = ", ".join([f"{t.type} ({t.year})" for t in node.transmission])
            feedback += f"- Transmission chain: {trans_info}\n"

        feedback += f"\nOther extant sources are closer to the topic anchor."

    return feedback

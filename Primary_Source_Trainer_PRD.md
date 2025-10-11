# PRD: Closest Extant Source Trainer

## Executive Summary
- **Goal**: Train and test recognition of primary vs secondary sources for early medieval topics using chain-of-transmission logic.
- **Core Mechanic**: Interactive graph connecting historical events to texts (extant/lost). Students classify nodes; grading rewards correct identification of the closest extant document.
- **Generator**: Produces historically plausible scenarios with time gaps, intermediaries, and reclassification logic when topic changes.
- **Deliverables**: Web app, instructor dashboard, auto-grading, rationale capture, and share link that emails results to **foxyaniv@gmail.com**.
- **Design**: Earth-tone minimalist SVG timeline. Event images + author icons. Arrows show mediation. Lost works as ghost nodes. No purple.

---

## 1. Problem Statement
Students often misidentify any old text as a primary source. This app teaches that, for a given inquiry, a *primary source* is the **closest extant document** to the historical event or phenomenon. Secondary literature analyzes or synthesizes. A text can change roles depending on the research topic.

---

## 2. Users and Goals
- **Students**: Learn to classify sources and explain reasoning.
- **Instructor**: Assign scenarios, set topics, review analytics, and receive emailed summaries.

---

## 3. Definitions
- **Event**: Historical occurrence (500–1000 CE).
- **Source Node**: Text/artifact with metadata: author role, year, place, transmission chain, extant/lost.
- **Primary (for topic)**: Extant nodes with minimal mediation depth to the event.
- **Secondary**: Nodes with greater mediation depth or that analyze others.
- **Topic Switch**: Reclassifies nodes relative to new inquiry anchor (e.g., historian’s perspective).

---

## 4. Learning Outcomes
- Distinguish primary vs secondary for specific topics.
- Understand mediation and extant status.
- Recognize reclassification when inquiry changes.

---

## 5. Core Interactions
1. **Scenario View**: Graph of event and sources along timeline. Students label each as Primary, Secondary, or Dependent on Topic. Provide justification.
2. **Topic Toggle**: Switch between topics (e.g., event vs reception). Labels update dynamically.
3. **Submission**: Instant grading and explanation. Share link emails summary to instructor.

---

## 6. Data Model
```json
{
  "event": {"id": "evt_lindisfarne_793", "title": "Raid on Lindisfarne", "year": 793, "place": "Northumbria", "image_url": "/img/lindisfarne.jpg"},
  "nodes": [
    {"id": "n1", "type": "text", "title": "Monk's letter describing the raid", "author_role": "eyewitness", "year": 794, "extant": true},
    {"id": "n2", "type": "text", "title": "Annals summarizing lost 794 letter", "author_role": "compiler", "year": 830, "extant": true, "transmission": [{"via": "lost_text", "year": 794}]}
  ],
  "edges": [
    {"from": "event", "to": "n1", "kind": "witness_record"},
    {"from": "event", "to": "ghost_794", "kind": "witness_record"},
    {"from": "ghost_794", "to": "n2", "kind": "summary_of_lost"}
  ],
  "topics": [
    {"id": "t_event", "label": "The raid itself (793)"},
    {"id": "t_reception9c", "label": "9th-century reception of the raid"}
  ]
}
```

---

## 7. Classification Algorithm
Shortest path from topic anchor (event or author) to each extant node defines **mediation depth**.

```python
def classify(nodes, edges, topic_anchor):
    G = build_graph(edges)
    extant = [n for n in nodes if n.extant]
    depths = {n.id: shortest_path_steps(G, topic_anchor, n.id) for n in extant}
    min_depth = min(depths.values())
    primary = {nid for nid, d in depths.items() if d == min_depth}
    secondary = set(n.id for n in extant) - primary
    return primary, secondary
```

Rules:
- Depth 0: contemporaneous artifact.
- Depth 1: eyewitness or first written record.
- +1 for each transmission (copy, summary, translation).
- Lost intermediaries count as mediation steps.

---

## 8. Scenario Generator
Produces historically coherent chains with varying depth and geography. Ensures plausible time gaps (5–200 years) and mediation types (summary, copy, translation).

**Examples**:
1. Eyewitness during event → primary.
2. Eyewitness writing decades later → still primary.
3. Lost 6th-c text → extant 9th-c summary → secondary.
4. Modern monograph → secondary, but primary for historian inquiry.

---

## 9. Grading Logic
- +1 per correct classification.
- +2 per correct justification containing keywords (e.g., *extant*, *lost*, *closest*).
- +1 for correct reclassification after topic switch.
- Normalized to 100.

Email includes: name, score, topic, misclassified nodes, and summary.

---

## 10. Instructor Dashboard
- Manage topics and difficulty.
- View analytics and common errors.
- Export CSV.

---

## 11. Accessibility and Localization
- Keyboard navigation.
- High-contrast palette.
- Alt text for icons.

---

## 12. Visual Design
- **Palette**: #F6F4F0 background, #2B2B2B text, #B2643C (event), #52796F (extant), #C0C7C4 (lost ghost), #84A98C (primary badge), #8D99AE (secondary badge). No purple.
- **Typography**: Inter + Vollkorn.
- **Icons**: Event (scene), Author (scribe).
- **Layout**: Horizontal SVG timeline with nodes by century.

---

### Example SVG
```html
<svg viewBox="0 0 1200 300">
  <line x1="100" y1="200" x2="1100" y2="200" stroke="#2B2B2B"/>
  <rect x="80" y="120" width="120" height="60" fill="#B2643C"/>
  <text x="140" y="155" fill="#F6F4F0" text-anchor="middle">Event 546</text>
  <rect x="400" y="120" width="150" height="60" fill="#C0C7C4" fill-opacity="0.2" stroke="#C0C7C4" stroke-dasharray="4 4"/>
  <rect x="800" y="120" width="180" height="60" fill="#52796F"/>
</svg>
```

---

## 13. Student Flow
1. Load scenario → classify nodes → toggle topic → submit → see score.
2. Receive explanation.
3. Share/email summary.

---

## 14. Tech Stack
- **Frontend**: React + D3/SVG.
- **Backend**: Node or Python (FastAPI).
- **Database**: Postgres.
- **Email**: Postmark or SendGrid.
- **Auth**: Magic link optional.

**API Endpoints**:
- `GET /api/scenario`
- `POST /api/grade`
- `POST /api/share`
- `GET /r/{token}`

---

## 15. Roadmap
- **MVP**: Scenario play, grading, topic toggle, email.
- **V1**: Dashboard + analytics.
- **V2**: Student-authored chains + peer review.

---

## 16. Visual Interaction Summary
- Hover: show tooltip (author, year, chain).
- Topic toggle: animate badge update.
- Keyboard: arrows to move focus, Enter to toggle.

---

## 17. Non-Functional Requirements
- Load <2s.
- Minimal tracking.
- Deterministic grading.
- FERPA/GDPR compliance.

---

## 18. Content Governance
- Historical plausibility required.
- No anachronisms.
- Use royalty-free imagery.

---

## 19. Implementation Notes
- Motion ≤150ms.
- Node width <220px.
- Minimal shadows, no gradients.
- Earth tones only.

---

## 20. Summary
This webapp evaluates conceptual understanding of *primary vs secondary* through interactive, historically grounded simulations. It visualizes transmission chains, enforces topic-dependent logic, and communicates results directly to the instructor.

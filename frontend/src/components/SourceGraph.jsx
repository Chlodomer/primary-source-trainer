import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

/**
 * Interactive graph visualization showing event-centric source relationships.
 * - Center circle = Event
 * - Connected circles = Sources (semi-transparent if lost/non-extant)
 * - Lines = Relationships between sources and event
 */
const SourceGraph = ({ scenario, selectedTopic }) => {
  const svgRef = useRef();

  useEffect(() => {
    if (!scenario || !svgRef.current) return;

    // Clear previous visualization
    d3.select(svgRef.current).selectAll('*').remove();

    const width = 800;
    const height = 600;
    const centerX = width / 2;
    const centerY = height / 2;

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .style('max-width', '100%')
      .style('height', 'auto');

    // Create event node at center
    const eventNode = {
      id: 'event',
      label: scenario.event.title,
      x: centerX,
      y: centerY,
      radius: 40,
      type: 'event'
    };

    // Create source nodes positioned in a circle around the event
    const sourceNodes = scenario.nodes.map((node, i) => {
      const angle = (i / scenario.nodes.length) * 2 * Math.PI;
      const distance = 200;
      return {
        id: node.id,
        label: node.title,
        x: centerX + distance * Math.cos(angle),
        y: centerY + distance * Math.sin(angle),
        radius: 30,
        type: 'source',
        extant: node.extant,
        nodeData: node
      };
    });

    const allNodes = [eventNode, ...sourceNodes];

    // Create edges based on scenario relationships
    const edges = [];

    // Add edges from sources to event
    scenario.nodes.forEach(node => {
      edges.push({
        source: node.id,
        target: 'event',
        type: 'relates_to'
      });
    });

    // Add edges between sources based on edges in scenario
    scenario.edges.forEach(edge => {
      edges.push({
        source: edge.from,
        target: edge.to,
        type: edge.kind
      });
    });

    // Draw edges
    const linkGroup = svg.append('g').attr('class', 'links');

    linkGroup.selectAll('line')
      .data(edges)
      .enter()
      .append('line')
      .attr('x1', d => {
        const sourceNode = allNodes.find(n => n.id === d.source);
        return sourceNode ? sourceNode.x : centerX;
      })
      .attr('y1', d => {
        const sourceNode = allNodes.find(n => n.id === d.source);
        return sourceNode ? sourceNode.y : centerY;
      })
      .attr('x2', d => {
        const targetNode = allNodes.find(n => n.id === d.target);
        return targetNode ? targetNode.x : centerX;
      })
      .attr('y2', d => {
        const targetNode = allNodes.find(n => n.id === d.target);
        return targetNode ? targetNode.y : centerY;
      })
      .attr('stroke', d => d.type === 'relates_to' ? '#84A98C' : '#B2643C')
      .attr('stroke-width', d => d.type === 'relates_to' ? 2 : 1.5)
      .attr('stroke-dasharray', d => d.type === 'relates_to' ? '0' : '5,5')
      .attr('opacity', 0.6);

    // Draw nodes
    const nodeGroup = svg.append('g').attr('class', 'nodes');

    const nodes = nodeGroup.selectAll('g')
      .data(allNodes)
      .enter()
      .append('g')
      .attr('transform', d => `translate(${d.x}, ${d.y})`)
      .style('cursor', 'pointer');

    // Add circles for nodes
    nodes.append('circle')
      .attr('r', d => d.radius)
      .attr('fill', d => {
        if (d.type === 'event') return '#B2643C';
        return '#52796F';
      })
      .attr('opacity', d => {
        if (d.type === 'event') return 1;
        return d.extant ? 0.9 : 0.3; // Semi-transparent for lost sources
      })
      .attr('stroke', d => d.type === 'event' ? '#8D4B2B' : '#3A5D54')
      .attr('stroke-width', 3);

    // Add labels
    nodes.append('text')
      .text(d => d.label)
      .attr('text-anchor', 'middle')
      .attr('dy', d => d.radius + 20)
      .attr('font-size', '12px')
      .attr('font-weight', d => d.type === 'event' ? 'bold' : 'normal')
      .attr('fill', '#2B2B2B')
      .style('pointer-events', 'none')
      .each(function(d) {
        const text = d3.select(this);
        const words = d.label.split(' ');
        text.text('');

        let line = [];
        let lineNumber = 0;
        const lineHeight = 14;
        const maxWidth = 100;

        words.forEach(word => {
          line.push(word);
          text.text(line.join(' '));
          if (text.node().getComputedTextLength() > maxWidth && line.length > 1) {
            line.pop();
            text.text(line.join(' '));
            text.append('tspan')
              .attr('x', 0)
              .attr('dy', lineHeight)
              .text(word);
            line = [word];
            lineNumber++;
          }
        });
      });

    // Add "LOST" indicator for non-extant sources
    nodes.filter(d => d.type === 'source' && !d.extant)
      .append('text')
      .text('LOST')
      .attr('text-anchor', 'middle')
      .attr('dy', 5)
      .attr('font-size', '10px')
      .attr('font-weight', 'bold')
      .attr('fill', 'white')
      .style('pointer-events', 'none');

    // Add tooltips
    const tooltip = d3.select('body')
      .append('div')
      .style('position', 'absolute')
      .style('background', 'rgba(0,0,0,0.8)')
      .style('color', 'white')
      .style('padding', '10px')
      .style('border-radius', '4px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('opacity', 0)
      .style('z-index', 1000);

    nodes.on('mouseover', function(event, d) {
      if (d.type === 'source') {
        tooltip
          .style('opacity', 1)
          .html(`
            <strong>${d.label}</strong><br/>
            <em>${d.nodeData.author_role}</em><br/>
            Year: ${d.nodeData.year}<br/>
            ${d.extant ? '✓ Extant' : '✗ Lost'}
          `);
      } else {
        tooltip
          .style('opacity', 1)
          .html(`
            <strong>${d.label}</strong><br/>
            <em>Event (${scenario.event.year} CE)</em><br/>
            ${scenario.event.place}
          `);
      }
    })
    .on('mousemove', function(event) {
      tooltip
        .style('left', (event.pageX + 15) + 'px')
        .style('top', (event.pageY - 15) + 'px');
    })
    .on('mouseout', function() {
      tooltip.style('opacity', 0);
    });

    // Cleanup tooltip on unmount
    return () => {
      tooltip.remove();
    };

  }, [scenario, selectedTopic]);

  return (
    <div style={{
      background: '#F6F4F0',
      padding: '20px',
      borderRadius: '8px',
      marginBottom: '20px',
      border: '2px solid #C0C7C4'
    }}>
      <h3 style={{ marginBottom: '15px', color: '#2B2B2B', textAlign: 'center' }}>
        Source Relationship Graph
      </h3>
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '20px',
        marginBottom: '15px',
        fontSize: '0.85rem',
        color: '#52796F'
      }}>
        <div>
          <span style={{
            display: 'inline-block',
            width: '20px',
            height: '20px',
            background: '#B2643C',
            borderRadius: '50%',
            marginRight: '5px',
            verticalAlign: 'middle'
          }}></span>
          Event
        </div>
        <div>
          <span style={{
            display: 'inline-block',
            width: '20px',
            height: '20px',
            background: '#52796F',
            borderRadius: '50%',
            marginRight: '5px',
            verticalAlign: 'middle',
            opacity: 0.9
          }}></span>
          Extant Source
        </div>
        <div>
          <span style={{
            display: 'inline-block',
            width: '20px',
            height: '20px',
            background: '#52796F',
            borderRadius: '50%',
            marginRight: '5px',
            verticalAlign: 'middle',
            opacity: 0.3
          }}></span>
          Lost Source
        </div>
      </div>
      <svg ref={svgRef}></svg>
    </div>
  );
};

export default SourceGraph;

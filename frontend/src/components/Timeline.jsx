import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const Timeline = ({ scenario, selectedTopic }) => {
  const svgRef = useRef();

  useEffect(() => {
    if (!scenario) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const width = 1200;
    const height = 300;
    const margin = { top: 40, right: 40, bottom: 40, left: 40 };

    svg.attr('viewBox', `0 0 ${width} ${height}`)
       .attr('preserveAspectRatio', 'xMidYMid meet');

    // Get year range
    const allYears = [
      scenario.event.year,
      ...scenario.nodes.map(n => n.year)
    ];
    const minYear = Math.min(...allYears) - 10;
    const maxYear = Math.max(...allYears) + 10;

    // Create scale
    const xScale = d3.scaleLinear()
      .domain([minYear, maxYear])
      .range([margin.left, width - margin.right]);

    const timelineY = height / 2;

    // Draw timeline axis
    svg.append('line')
      .attr('x1', margin.left)
      .attr('y1', timelineY)
      .attr('x2', width - margin.right)
      .attr('y2', timelineY)
      .attr('stroke', '#2B2B2B')
      .attr('stroke-width', 2);

    // Draw century markers
    const startCentury = Math.floor(minYear / 100) * 100;
    const endCentury = Math.ceil(maxYear / 100) * 100;

    for (let year = startCentury; year <= endCentury; year += 100) {
      const x = xScale(year);

      svg.append('line')
        .attr('x1', x)
        .attr('y1', timelineY - 10)
        .attr('x2', x)
        .attr('y2', timelineY + 10)
        .attr('stroke', '#2B2B2B')
        .attr('stroke-width', 1);

      svg.append('text')
        .attr('x', x)
        .attr('y', timelineY + 30)
        .attr('text-anchor', 'middle')
        .attr('fill', '#8D99AE')
        .attr('font-size', '12px')
        .text(`${year} CE`);
    }

    // Draw event
    const eventX = xScale(scenario.event.year);
    const eventGroup = svg.append('g')
      .attr('transform', `translate(${eventX}, ${timelineY - 80})`);

    eventGroup.append('rect')
      .attr('x', -60)
      .attr('y', 0)
      .attr('width', 120)
      .attr('height', 50)
      .attr('fill', '#B2643C')
      .attr('rx', 4);

    eventGroup.append('text')
      .attr('x', 0)
      .attr('y', 25)
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'middle')
      .attr('fill', '#F6F4F0')
      .attr('font-size', '12px')
      .attr('font-weight', '600')
      .text('EVENT')
      .call(wrap, 110);

    eventGroup.append('text')
      .attr('x', 0)
      .attr('y', -15)
      .attr('text-anchor', 'middle')
      .attr('fill', '#2B2B2B')
      .attr('font-size', '11px')
      .attr('font-weight', '600')
      .text(scenario.event.year);

    // Draw nodes
    scenario.nodes.forEach((node, i) => {
      const nodeX = xScale(node.year);
      const nodeY = i % 2 === 0 ? timelineY - 80 : timelineY + 50;

      const nodeGroup = svg.append('g')
        .attr('transform', `translate(${nodeX}, ${nodeY})`)
        .attr('class', 'node-group')
        .style('cursor', 'pointer');

      // Node rectangle
      const rectWidth = 140;
      const rectHeight = 60;

      nodeGroup.append('rect')
        .attr('x', -rectWidth / 2)
        .attr('y', 0)
        .attr('width', rectWidth)
        .attr('height', rectHeight)
        .attr('fill', node.extant ? '#52796F' : '#C0C7C4')
        .attr('fill-opacity', node.extant ? 1 : 0.3)
        .attr('stroke', node.extant ? 'none' : '#C0C7C4')
        .attr('stroke-dasharray', node.extant ? 'none' : '4 4')
        .attr('stroke-width', 2)
        .attr('rx', 4);

      // Node title
      nodeGroup.append('text')
        .attr('x', 0)
        .attr('y', 20)
        .attr('text-anchor', 'middle')
        .attr('fill', node.extant ? '#F6F4F0' : '#8D99AE')
        .attr('font-size', '10px')
        .attr('font-weight', '500')
        .text(node.title.substring(0, 30) + (node.title.length > 30 ? '...' : ''))
        .call(wrap, rectWidth - 10);

      // Node year badge - only show if different from event year
      if (node.year !== scenario.event.year) {
        nodeGroup.append('text')
          .attr('x', 0)
          .attr('y', -8)
          .attr('text-anchor', 'middle')
          .attr('fill', '#2B2B2B')
          .attr('font-size', '10px')
          .attr('font-weight', '600')
          .text(node.year);
      }

      // Lost badge
      if (!node.extant) {
        nodeGroup.append('text')
          .attr('x', 0)
          .attr('y', 50)
          .attr('text-anchor', 'middle')
          .attr('fill', '#8D99AE')
          .attr('font-size', '9px')
          .attr('font-style', 'italic')
          .text('(lost)');
      }

      // Connection line to timeline
      nodeGroup.append('line')
        .attr('x1', 0)
        .attr('y1', rectHeight)
        .attr('x2', 0)
        .attr('y2', i % 2 === 0 ? 80 - nodeY + timelineY : timelineY - nodeY)
        .attr('stroke', '#C0C7C4')
        .attr('stroke-width', 1)
        .attr('stroke-dasharray', '2 2');

      // Tooltip on hover
      nodeGroup.append('title')
        .text(`${node.title}\n${node.author_role} (${node.year})\n${node.extant ? 'Extant' : 'Lost'}`);
    });

    // Helper function to wrap text
    function wrap(text, width) {
      text.each(function() {
        const text = d3.select(this);
        const words = text.text().split(/\s+/).reverse();
        let word;
        let line = [];
        let lineNumber = 0;
        const lineHeight = 1.1;
        const y = text.attr('y');
        const dy = 0;
        let tspan = text.text(null).append('tspan').attr('x', 0).attr('y', y).attr('dy', dy + 'em');

        while (word = words.pop()) {
          line.push(word);
          tspan.text(line.join(' '));
          if (tspan.node().getComputedTextLength() > width) {
            line.pop();
            tspan.text(line.join(' '));
            line = [word];
            tspan = text.append('tspan').attr('x', 0).attr('y', y).attr('dy', ++lineNumber * lineHeight + dy + 'em').text(word);
          }
        }
      });
    }

  }, [scenario, selectedTopic]);

  return (
    <div className="timeline-container">
      <svg ref={svgRef} style={{ width: '100%', height: 'auto' }}></svg>
    </div>
  );
};

export default Timeline;

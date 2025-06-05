import React, { useEffect, useRef } from 'react';
import cloud from 'd3-cloud';
import * as d3 from 'd3';

function WordCloudChart({ words }) {
  const svgRef = useRef();

  useEffect(() => {
    if (!words || words.length === 0) return;

    const layout = cloud()
      .size([500, 300])
      .words(words.map(d => ({ text: d.text, size: d.value * 10 })))
      .padding(5)
      .rotate(() => ~~(Math.random() * 2) * 90)
      .font('Impact')
      .fontSize(d => d.size)
      .on('end', draw);

    layout.start();

    function draw(words) {
      const svg = d3.select(svgRef.current);
      svg.selectAll('*').remove(); // Clear previous render

      svg
        .attr('width', layout.size()[0])
        .attr('height', layout.size()[1])
        .append('g')
        .attr('transform', `translate(${layout.size()[0] / 2},${layout.size()[1] / 2})`)
        .selectAll('text')
        .data(words)
        .enter()
        .append('text')
        .style('font-family', 'Impact')
        .style('fill', () => d3.schemeCategory10[Math.floor(Math.random() * 10)])
        .style('font-size', d => `${d.size}px`)
        .attr('text-anchor', 'middle')
        .attr('transform', d => `translate(${d.x},${d.y})rotate(${d.rotate})`)
        .text(d => d.text);
    }
  }, [words]);

  return <svg ref={svgRef} />;
}

export default WordCloudChart;

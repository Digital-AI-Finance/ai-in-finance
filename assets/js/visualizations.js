// =============================================================================
// VISUALIZATIONS - Research Project Analytics
// =============================================================================
// This file creates interactive charts and graphs for the analytics section
// Requires Chart.js for bar charts and D3.js for network graphs

document.addEventListener('DOMContentLoaded', function() {
  // Only initialize if the elements exist
  if (document.getElementById('pubsChart')) {
    initPublicationsChart();
  }
  if (document.getElementById('networkGraph')) {
    initNetworkGraph();
  }
});

// =============================================================================
// PUBLICATIONS CHART (Chart.js)
// =============================================================================

function initPublicationsChart() {
  const ctx = document.getElementById('pubsChart');
  if (!ctx || typeof Chart === 'undefined') return;

  // Count publications by year from publicationsData (set in index.md)
  const yearCounts = {};
  if (typeof publicationsData !== 'undefined') {
    publicationsData.forEach(pub => {
      if (pub.year) {
        yearCounts[pub.year] = (yearCounts[pub.year] || 0) + 1;
      }
    });
  }

  const years = Object.keys(yearCounts).sort();
  const counts = years.map(y => yearCounts[y]);

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: years,
      datasets: [{
        label: 'Publications',
        data: counts,
        // Customize colors to match your theme
        backgroundColor: 'var(--primary-color, #1a365d)',
        borderColor: 'var(--primary-dark, #0f2942)',
        borderWidth: 1,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 5 }
        }
      }
    }
  });
}

// =============================================================================
// NETWORK GRAPH (D3.js)
// =============================================================================
// Customize nodes and links to show your team's collaboration network

function initNetworkGraph() {
  const container = document.getElementById('networkGraph');
  if (!container || typeof d3 === 'undefined') return;

  const width = container.clientWidth || 300;
  const height = 200;

  // Create SVG
  const svg = d3.select('#networkGraph')
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  // ==========================================================================
  // CUSTOMIZE YOUR NETWORK DATA HERE
  // ==========================================================================
  // Nodes: team members (group 1 = core team, group 2 = collaborators)
  const nodes = [
    { id: 'PI', name: 'Principal Investigator', group: 1 },
    { id: 'R1', name: 'Researcher 1', group: 1 },
    { id: 'R2', name: 'Researcher 2', group: 1 },
    { id: 'R3', name: 'Researcher 3', group: 1 },
    { id: 'C1', name: 'Collaborator 1', group: 2 },
    { id: 'C2', name: 'Collaborator 2', group: 2 }
  ];

  // Links: co-authorship or collaboration connections
  // value = strength of connection (e.g., number of co-authored papers)
  const links = [
    { source: 'PI', target: 'R1', value: 5 },
    { source: 'PI', target: 'R2', value: 4 },
    { source: 'PI', target: 'R3', value: 3 },
    { source: 'R1', target: 'R2', value: 3 },
    { source: 'R2', target: 'R3', value: 2 },
    { source: 'PI', target: 'C1', value: 2 },
    { source: 'PI', target: 'C2', value: 1 }
  ];
  // ==========================================================================

  // Create force simulation
  const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(50))
    .force('charge', d3.forceManyBody().strength(-100))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(25));

  // Draw links
  const link = svg.append('g')
    .selectAll('line')
    .data(links)
    .join('line')
    .attr('stroke', '#c9a227')  // accent color
    .attr('stroke-opacity', 0.6)
    .attr('stroke-width', d => Math.sqrt(d.value));

  // Draw nodes
  const node = svg.append('g')
    .selectAll('circle')
    .data(nodes)
    .join('circle')
    .attr('r', d => d.group === 1 ? 12 : 8)  // core team larger
    .attr('fill', d => d.group === 1 ? '#1a365d' : '#718096')  // primary color vs gray
    .attr('stroke', '#c9a227')  // accent color border
    .attr('stroke-width', 2)
    .call(drag(simulation));

  // Add labels
  const label = svg.append('g')
    .selectAll('text')
    .data(nodes)
    .join('text')
    .text(d => d.id)
    .attr('font-size', '8px')
    .attr('fill', '#2d3748')
    .attr('text-anchor', 'middle')
    .attr('dy', 20);

  // Add tooltips
  node.append('title').text(d => d.name);

  // Update positions on tick
  simulation.on('tick', () => {
    link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y);

    node
      .attr('cx', d => d.x)
      .attr('cy', d => d.y);

    label
      .attr('x', d => d.x)
      .attr('y', d => d.y);
  });

  // Drag interaction functions
  function drag(simulation) {
    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    return d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended);
  }
}

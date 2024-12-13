// Set up dimensions and margins
const margin = { top: 20, right: 40, bottom: 60, left: 60 };
const width = window.innerWidth - margin.left - margin.right;  
const height = window.innerHeight - margin.top - margin.bottom;

// Append SVG to the DOM
const svg = d3.select("#scatterplot").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Load the CSV data
d3.csv("../data/enao-genres.csv").then(function(data) {

    // Parse numeric values from strings
    data.forEach(d => {
        d.top_pixel = +d.top_pixel;
        d.left_pixel = +d.left_pixel;
        d.font_size = +d.font_size;
        d.color = d.color || "#69b3a2"; // Default color
    });

    // Set scales for x, y, and font_size (radius)
    const x = d3.scaleLinear()
        .domain([d3.min(data, d => d.left_pixel) - 150, d3.max(data, d => d.left_pixel) + 150])
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([d3.min(data, d => d.top_pixel) - 1500, d3.max(data, d => d.top_pixel) + 1500])
        .range([0, height]);

    // Scale font_size to circle radius (use sqrt scale)
    const radius = d3.scaleSqrt()
        .domain([d3.min(data, d => d.font_size), d3.max(data, d => d.font_size)])
        .range([4, 16]);  // Circle sizes

    // Create density function for contours
    const density = d3.contourDensity()
        .x(d => x(d.left_pixel))
        .y(d => y(d.top_pixel))
        .size([width, height])
        .thresholds(30)
        .bandwidth(40);

    // Create color scale for contours
    const color = d3.scaleLinear().domain(d3.extent(density(data), d => d.value)).range(["#06D6A0", "#EF476F"]);

    // Function to create the chart (scatter plot + contours)
    function drawChart(w_masks) {
        // Clear previous chart elements
        svg.selectAll("*").remove();

        // Create circles for scatter plot
        svg.append("g")
            .selectAll(".dot")
            .data(data)
            .enter().append("circle")
            .attr("class", "dot")
            .attr("cx", d => x(d.left_pixel))
            .attr("cy", d => y(d.top_pixel))
            .attr("r", d => radius(d.font_size))
            .attr("fill", d => d.color)
            .on("mouseover", function(event, d) {
                const tooltip = d3.select("#tooltip");
                tooltip.style("visibility", "visible")
                    .html(`<strong>Genre:</strong> ${d.genre_name}<br>
                           <strong>Preview:</strong> <a href="${d.preview_url}" target="_blank">Listen</a>`)
                    .style("top", `${event.pageY + 5}px`)
                    .style("left", `${event.pageX + 5}px`);
            })
            .on("mouseout", function() {
                d3.select("#tooltip").style("visibility", "hidden");
            })
            .on("click", function(event, d) {
                // Toggle selected state on click
                d3.select(this).classed("selected", !d3.select(this).classed("selected"));
            });

        // Generate contours
        const contours = density(data);

        // Create contour paths with optional clipping mask
        const contourGroup = svg.append("g")
            .selectAll(".contour")
            .data(contours)
            .enter().append("path")
            .attr("class", "contour")
            .attr("d", d3.geoPath())
            .attr("stroke-width", 2)
            .attr("stroke", d => color(d.value))
            .attr("stroke-linejoin", "round")
            .style("fill", d => {
                return w_masks ? `url(#mask${d.ix})` : color(d.value).replace(")", ", 0.3)");  // Apply mask or fill color
            });

        if (w_masks) {
            // Create clipping masks for contours
            const masks = svg.append("defs")
                .selectAll("mask")
                .data(contours)
                .enter().append("mask")
                .attr("id", (d, i) => "mask" + i);

            masks.append("path")
                .attr("d", d3.geoPath())
                .style("fill", "white");

            masks.append("path")
                .attr("d", d => d3.geoPath())
                .style("fill", "black");
        }
    }

    // Initial chart render with clipping masks enabled (checkbox default state is checked)
    drawChart(true);

    // Event listener for checkbox to toggle `w_masks`
    document.getElementById("toggle-mask").addEventListener("change", function() {
        drawChart(this.checked); // Re-draw chart based on checkbox state
    });

});

// Window resize event to make the chart responsive
window.addEventListener("resize", function() {
    location.reload(); // Reload the page on resize to adapt the layout
});
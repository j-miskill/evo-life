
// Automatically populating health metrics
document.addEventListener("DOMContentLoaded", function () {
    const dropdownUserId = document.getElementById("user_id");
    const dropdownMetricDate = document.getElementById("metric_date");  
    const healthMetricsTable = document.querySelector("#health-metrics-table");
    const healthMetricsBody = document.querySelector("#health-metrics-table tbody");
    const welcomeMessage = document.getElementById("welcome-message");

    function fetchMetrics(user_id, metric_date) {
        fetch(`/get_metrics/${user_id}/${metric_date}`)
            .then(response => response.json())
            .then(data => {
                // Clear previous rows
                healthMetricsBody.innerHTML = "";

                if (data.length > 0) {
                    // Populate table with new data
                    data.forEach(metric => {
                        const row = document.createElement("tr");
                        row.innerHTML = `
                            <td>${metric.nremhr}</td>
                            <td>${metric.rmssd}</td>
                            <td>${metric.spo2}</td>
                            <td>${metric.exertion_points_percentage}</td>
                            <td>${metric.responsiveness_points_percentage}</td>
                            <td>${metric.distance}</td>
                            <td>${metric.activityType}</td>
                            <td>${metric.bpm}</td>
                            <td>${metric.lightly_active_minutes}</td>
                            <td>${metric.moderately_active_minutes}</td>
                            <td>${metric.very_active_minutes}</td>
                            <td>${metric.sedentary_minutes}</td>
                            <td>${metric.mindfulness_session}</td>
                            <td>${metric.sleep_duration}</td>
                            <td>${metric.minutesAsleep}</td>
                            <td>${metric.minutesAwake}</td>
                            <td>${metric.sleep_efficiency}</td>
                            <td>${metric.gender}</td>
                            <td>${metric.bmi}</td>
                            <td>${metric.gym}</td>
                            <td>${metric.home}</td>
                            <td>${metric.outdoors}</td>

                            <td class="phenotype">${metric.stress_score}</td>
                            <td class="phenotype">${metric.sleep_points_percentage}</td>
                            <td class="phenotype">${metric.tense_anxious}</td>
                            <td class="phenotype">${metric.tired}</td>
                        `;
                        healthMetricsBody.appendChild(row);
                    });

                    // Show the table
                    healthMetricsTable.style.display = "table";
                    welcomeMessage.textContent = `Welcome, User ${user_id}!`;
                } else {
                    // No data for selected user
                    welcomeMessage.textContent = `No health metrics found for User ${user_id}.`;
                    healthMetricsTable.style.display = "none";
                }
            })
            .catch(error => {
                console.error("Error fetching metrics:", error);
                welcomeMessage.textContent = `Failed to fetch health metrics.`;
                healthMetricsTable.style.display = "none";
            });
    }

    // Add event listener for user_id dropdown
    dropdownUserId.addEventListener("change", function () {
        const selectedUserId = dropdownUserId.value;
        const selectedMetricDate = dropdownMetricDate.value;  // Get the selected metric date

        // Only fetch data if both user_id and metric_date are selected
        if (selectedUserId && selectedMetricDate) {
            fetchMetrics(selectedUserId, selectedMetricDate);
        } else {
            // Hide table and clear message if not both are selected
            healthMetricsTable.style.display = "none";
            welcomeMessage.textContent = "";
        }
    });

    // Add event listener for metric_date dropdown if necessary
    dropdownMetricDate.addEventListener("change", function () {
        const selectedUserId = dropdownUserId.value;  // Get the selected user ID
        const selectedMetricDate = dropdownMetricDate.value;

        // Only fetch data if both user_id and metric_date are selected
        if (selectedUserId && selectedMetricDate) {
            fetchMetrics(selectedUserId, selectedMetricDate);
        } else {
            // Hide table and clear message if not both are selected
            healthMetricsTable.style.display = "none";
            welcomeMessage.textContent = "";
        }
    });
});



// Function to create twisting strands with animation
function createAnimatedGeneStrands(encodings) {
    const geneVisualization = document.getElementById('gene-visualization');
    geneVisualization.innerHTML = ''; // Clear existing elements

    const strandHeight = 400; // Height of the container
    const totalNodes = encodings.length;
    const amplitude = 50; // Amplitude of the sine wave
    const frequency = 0.5; // Frequency of the sine wave
    const offsetX = 100; // Horizontal offset between strands

    // Create an array to store node elements for animation
    const nodes = [];
    const lines = [];

    // Loop through encodings and position circles along the strands
    for (let i = 0; i < totalNodes; i++) {
        const y = (i / totalNodes) * strandHeight; // Distribute circles vertically

        // Create the first strand circle
        const circle1 = document.createElement('div');
        circle1.className = 'gene-box gene-strand1'; // Add a class for strand 1
        circle1.style.top = `${y}px`;
        circle1.textContent = encodings[i];
        geneVisualization.appendChild(circle1);
        nodes.push({ element: circle1, isStrand1: true, index: i });

        // Create the second strand circle
        if (encodings[i + 1] !== undefined) {
            const circle2 = document.createElement('div');
            circle2.className = 'gene-box gene-strand2'; // Add a class for strand 2
            circle2.style.top = `${y}px`;
            circle2.textContent = encodings[i + 1];
            geneVisualization.appendChild(circle2);
            nodes.push({ element: circle2, isStrand1: false, index: i + 1 });

            // Create the connecting line
            const line = document.createElement('div');
            line.className = 'gene-line';
            geneVisualization.appendChild(line);
            lines.push({ element: line, top: y });
            i++; // Skip the next encoding, as it's already used
        }
    }

    // Animate the nodes and lines
    let angle = 10; // Initial angle for the sine wave
    function animateGene() {
        angle += 0.025; // Increment the angle for animation

        // Update node positions
        nodes.forEach((node) => {
            const strandOffset = node.isStrand1 ? 0 : Math.PI; // Offset for the second strand
            const x = amplitude * Math.sin(angle + node.index * frequency + strandOffset) + (node.isStrand1 ? offsetX : offsetX + 2 * amplitude);
            node.element.style.left = `${x}px`;
        });

        // Update line lengths and positions
        lines.forEach((line, index) => {
            const node1 = nodes[index * 2];
            const node2 = nodes[index * 2 + 1];
            const x1 = parseFloat(node1.element.style.left);
            const x2 = parseFloat(node2.element.style.left);
            const centerX1 = x1 + 10; // Center X of circle 1
            const centerX2 = x2 + 10; // Center X of circle 2
            const centerY = line.top + 15; // Center Y of circles
            const length = Math.abs(centerX2 - centerX1); // Distance between the circles

            // Update line position and size
            line.element.style.top = `${centerY}px`;
            line.element.style.left = `${Math.min(centerX1, centerX2)}px`;
            line.element.style.width = `${length}px`;
        });

        requestAnimationFrame(animateGene); // Repeat the animation
    }

    animateGene(); // Start the animation
}


// Fetch Gene Encodings from DB
document.addEventListener("DOMContentLoaded", function () {
    const dropdownUserId = document.getElementById("user_id");
    const dropdownMetricDate = document.getElementById("metric_date"); 
    const geneVisualization = document.getElementById('gene-visualization');

    function fetchEncodings(user_id, metric_date) { 

        const encodings = [];

        fetch(`/get_encodings/${user_id}/${metric_date}`)
            .then(response => response.json())
            .then(data => {

                // Check if the data is an array and has items
                if (data.length > 0) {

                    // Iterate through each encoding object in the data array
                    data.forEach(encoding => {
                        // Push the values from each encoding object to the encodings array
                        
                        encodings.push(
                            encoding.encoded_gender,
                            encoding.encoded_nremhr,
                            encoding.encoded_rmssd,
                            encoding.encoded_spo2,
                            encoding.encoded_exertion_points_percentage,
                            encoding.encoded_responsiveness_points_percentage,
                            encoding.encoded_distance,
                            encoding.encoded_activityType,
                            encoding.encoded_bpm,
                            encoding.encoded_lightly_active_minutes,
                            encoding.encoded_moderately_active_minutes,
                            encoding.encoded_very_active_minutes,
                            encoding.encoded_sedentary_minutes,
                            encoding.encoded_mindfulness_session,
                            encoding.encoded_sleep_duration,
                            encoding.encoded_minutesAsleep,
                            encoding.encoded_minutesAwake,
                            encoding.encoded_sleep_efficiency,
                            encoding.encoded_bmi,
                            encoding.encoded_gym,
                            encoding.encoded_home,
                            encoding.encoded_outdoors

                        );
                        
                        //encodings.push(encodingValues);

                    });

                    // Now pass the encodings array to your gene strand creation function
                    createAnimatedGeneStrands(encodings);

                } else {
                    console.error("No valid data found or data is not in expected format");
                }

            })
            .catch(error => {
                console.error("Error fetching Encodings:", error);
                welcomeMessage.textContent = `Failed to fetch health Encodings.`;
            });
    }

    // Add event listener for user_id dropdown
    dropdownUserId.addEventListener("change", function () {
        const selectedUserId = dropdownUserId.value;
        const selectedMetricDate = dropdownMetricDate.value;  // Get the selected metric date

        // Only fetch data if both user_id and metric_date are selected
        if (selectedUserId && selectedMetricDate) {
            fetchEncodings(selectedUserId, selectedMetricDate);
        } else {
            // Hide table and clear message if not both are selected
            welcomeMessage.textContent = "";
        }
    });

    // Add event listener for metric_date dropdown if necessary
    dropdownMetricDate.addEventListener("change", function () {
        const selectedUserId = dropdownUserId.value;  // Get the selected user ID
        const selectedMetricDate = dropdownMetricDate.value;

        // Only fetch data if both user_id and metric_date are selected
        if (selectedUserId && selectedMetricDate) {
            fetchEncodings(selectedUserId, selectedMetricDate);
        } else {
            // Hide table and clear message if not both are selected
            geneVisualization.style.display = "none";
            welcomeMessage.textContent = "";
        }
    });
});

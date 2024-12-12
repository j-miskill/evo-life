
//HEALTH METRIC LOGIC

// Automatically populating health metrics
document.addEventListener("DOMContentLoaded", function () {
    const dropdownUserId = document.getElementById("user_id");
    const dropdownMetricDate = document.getElementById("month");  
    const healthMetricsTable = document.querySelector("#health-metrics-table");
    const healthMetricsBody = document.querySelector("#health-metrics-table tbody");
    const welcomeMessage = document.getElementById("welcome-message");

    function fetchMetrics(user_id, month) {
        fetch(`/get_metrics/${user_id}/${month}`)
            .then(response => response.json())
            .then(data => {
                // Clear previous rows
                healthMetricsBody.innerHTML = "";

                if (data.length > 0) {
                    // Populate table with new data
                    data.forEach(metric => {
                        const row = document.createElement("tr");
                        row.innerHTML = `
                            <td>${metric.date}</td>
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

        // Only fetch data if both user_id and month are selected
        if (selectedUserId && selectedMetricDate) {
            fetchMetrics(selectedUserId, selectedMetricDate);
        } else {
            // Hide table and clear message if not both are selected
            healthMetricsTable.style.display = "none";
            welcomeMessage.textContent = "";
        }
    });

    // Add event listener for month dropdown if necessary
    dropdownMetricDate.addEventListener("change", function () {
        const selectedUserId = dropdownUserId.value;  // Get the selected user ID
        const selectedMetricDate = dropdownMetricDate.value;

        // Only fetch data if both user_id and month are selected
        if (selectedUserId && selectedMetricDate) {
            fetchMetrics(selectedUserId, selectedMetricDate);
        } else {
            // Hide table and clear message if not both are selected
            healthMetricsTable.style.display = "none";
            welcomeMessage.textContent = "";
        }
    });
});



// GENOTYPE LOGIC

function createAnimatedGeneStrands(encodings, encoding_sums) {
    const geneVisualization = document.getElementById('gene-visualization');
    geneVisualization.innerHTML = ''; // Clear existing elements

    const strandHeight = 350; // Height of the container
    const totalNodes = encodings.length;
    const amplitude = 80; // Amplitude of the sine wave
    const frequency = 0.3; // Frequency of the sine wave
    const offsetX = 150; // Horizontal offset between strands

    const nodes = [];
    const lines = [];
    const lineColors = [];
    const lineTextColors = [];


    // Define the min and max sum for normalization
    const minSum = 50;  // Adjust this based on your expected minimum sum
    const maxSum = 150; // Adjust this based on your expected maximum sum


    // Calculate the sum of the encodings

    for (let i = 0; i < encoding_sums.length; i++) {

        const sum = encoding_sums[i];

        // Normalize the sum to a range of 0 to 1
        const normalizedSum = Math.max(0, Math.min((sum - minSum) / (maxSum - minSum), 1));

        const red = Math.round(255 * (1 - normalizedSum)); // More red for lower normalized scores
        const green = Math.round(255 * normalizedSum);    // More green for higher normalized scores

        lineColors.push(`rgb(${red}, ${green}, 0)`);
        lineTextColors.push(`rgb(${red}, ${green}, 0, 0.4)`);


    };
    

    // Loop through encodings and position elements
    for (let i = 0; i < totalNodes; i++) {
        const y = (i / totalNodes) * strandHeight; // Distribute vertically

        // Create the first strand circle
        const circle1 = document.createElement('div');
        circle1.className = 'gene-box gene-strand1';
        circle1.style.top = `${y}px`;
        geneVisualization.appendChild(circle1);
        nodes.push({ element: circle1, isStrand1: true, index: i });

        // Create the second strand circle
        const circle2 = document.createElement('div');
        circle2.className = 'gene-box gene-strand2';
        circle2.style.top = `${y}px`;
        geneVisualization.appendChild(circle2);
        nodes.push({ element: circle2, isStrand1: false, index: i });

        // Create a connecting line
        const line = document.createElement('div');
        line.className = 'gene-line';
        line.style.backgroundColor = `${lineColors[i]}`; // Set line color dynamically
        geneVisualization.appendChild(line);

        // Add encoding text to the line
        const lineText = document.createElement('div');
        lineText.className = 'line-text';
        lineText.textContent = encodings[i];
        lineText.style.color = `${lineTextColors[i]}`;
        geneVisualization.appendChild(lineText);

        lines.push({ element: line, text: lineText, top: y });
    }

    // Animate the nodes and lines
    let angle = 0;
    function animateGene() {
        angle += 0.03;

        nodes.forEach((node) => {
            const strandOffset = node.isStrand1 ? 0 : Math.PI; // Offset for the second strand
            const x = amplitude * Math.sin(angle + node.index * frequency + strandOffset) +
                      (node.isStrand1 ? offsetX : offsetX + 2 * amplitude);
            node.element.style.left = `${x}px`;
        });

        lines.forEach((line, index) => {
            const node1 = nodes[index * 2];
            const node2 = nodes[index * 2 + 1];
            const x1 = parseFloat(node1.element.style.left);
            const x2 = parseFloat(node2.element.style.left);
            const y = line.top + 15;

            const length = Math.sqrt((x2 - x1) ** 2 + 30 ** 2);
            const angle = Math.atan2(30, x2 - x1) * (180 / Math.PI);

            line.element.style.top = `${y}px`;
            line.element.style.left = `${Math.min(x1, x2)}px`;
            line.element.style.width = `${length}px`;
            line.element.style.transform = `rotate(${angle}deg)`;

            // Position encoding text
            const textX = (x1 + x2) / 2;
            line.text.style.top = `${y + 5}px`;
            line.text.style.left = `${textX + 0}px`;
        });

        requestAnimationFrame(animateGene);
    }

    animateGene();
}


// Fetch Gene Encodings from DB
document.addEventListener("DOMContentLoaded", function () {
    const dropdownUserId = document.getElementById("user_id");
    const dropdownMetricDate = document.getElementById("month");

    function fetchEncodings(user_id, month) {
        fetch(`/get_encodings/${user_id}/${month}`)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    const encodings = data.map(item => item.encoding);
                    const encoding_sums = data.map(item => item.encoding_sum);
                    createAnimatedGeneStrands(encodings, encoding_sums);
                }
            })
            .catch(error => {
                console.error("Error fetching Encodings:", error);
            });
    }

    dropdownUserId.addEventListener("change", function () {
        const userId = dropdownUserId.value;
        const month = dropdownMetricDate.value;
        if (userId && month) fetchEncodings(userId, month);
    });

    dropdownMetricDate.addEventListener("change", function () {
        const userId = dropdownUserId.value;
        const month = dropdownMetricDate.value;
        if (userId && month) fetchEncodings(userId, month);
    });
});


// PHENOTYPE LOGIC

// Automatically populating phenotype score
document.addEventListener("DOMContentLoaded", function () {
    const dropdownUserId = document.getElementById("user_id");
    const dropdownMetricDate = document.getElementById("month");  
    const phenotypeVisualization = document.getElementById("phenotype-visualization");

    function fetchPhenotype(user_id, month) {
        fetch(`/get_phenotypes/${user_id}/${month}`)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    const phenotypeScore = parseFloat(data[0].phenotype_score);
                    phenotypeVisualization.innerHTML = `<h2>${phenotypeScore.toFixed(2)}</h2>`;

                    // Normalize the score to map to the red-green scale
                    const normalizedScore = Math.max(0, Math.min((phenotypeScore - 0.45) / 0.6, 1)); // Scale 0.6 to 1.0 to 0-1
                    const red = Math.round(255 * (1 - normalizedScore)); // More red for lower normalized scores
                    const green = Math.round(255 * normalizedScore);    // More green for higher normalized scores

                    phenotypeVisualization.style.backgroundColor = `rgb(${red}, ${green}, 0)`;
                    phenotypeVisualization.style.color = phenotypeScore > 0.5 ? "black" : "white"; // Adjust text color for contrast
                } else {
                    phenotypeVisualization.innerHTML = `<h3>No phenotype score available for the selected user and month.</h3>`;
                    phenotypeVisualization.style.backgroundColor = "transparent"; // Reset to default
                }
            })
            .catch(error => {
                console.error("Error fetching phenotype score:", error);
                phenotypeVisualization.innerHTML = `<h3>Failed to fetch phenotype score.</h3>`;
                phenotypeVisualization.style.backgroundColor = "transparent"; // Reset to default
            });
    }

    // Add event listeners for user_id and month dropdowns
    dropdownUserId.addEventListener("change", function () {
        const selectedUserId = dropdownUserId.value;
        const selectedMetricDate = dropdownMetricDate.value;

        if (selectedUserId && selectedMetricDate) {
            fetchPhenotype(selectedUserId, selectedMetricDate);
        } else {
            phenotypeVisualization.innerHTML = "";
        }
    });

    dropdownMetricDate.addEventListener("change", function () {
        const selectedUserId = dropdownUserId.value;
        const selectedMetricDate = dropdownMetricDate.value;

        if (selectedUserId && selectedMetricDate) {
            fetchPhenotype(selectedUserId, selectedMetricDate);
        } else {
            phenotypeVisualization.innerHTML = "";
        }
    });
});



// HEALTH TRENDS

document.addEventListener("DOMContentLoaded", function () {
    const dropdownUserId = document.getElementById("user_id");
    if (!dropdownUserId) {
        console.error("Dropdown element with ID 'user_id' not found.");
        return;
    }

    let healthChart;

    function fetchHealthTrends(userId) {
        fetch(`/get_metric_trends/${userId}`)
            .then(response => response.json())
            .then(healthData => {
                const labels = healthData.map(item => item.date);
                const sleep_efficiency = healthData.map(item => item.sleep_efficiency);
                const distance = healthData.map(item => item.distance/100);
                const bpm = healthData.map(item => item.bpm);
                const sedentary_minutes = healthData.map(item => item.sedentary_minutes/10);
                const total_active = healthData.map(item => (item.lightly_active_minutes + item.moderately_active_minutes + item.very_active_minutes)/10);

                updateChart(labels, [
                    {
                        label: 'Sleep Efficiency',
                        data: sleep_efficiency,
                        borderColor: '#1984c5',
                        fill: false,
                    },
                    {
                        label: 'Distance/100',
                        data: distance,
                        borderColor: '#87bc45',
                        fill: false,
                    },
                    {
                        label: 'Heart Rate',
                        data: bpm,
                        borderColor: '#c23728',
                        fill: false,
                    },
                    {
                        label: 'Sedentary Mins/10',
                        data: sedentary_minutes,
                        borderColor: '#beb9db',
                        fill: false,
                    },
                    {
                        label: 'Active Mins/10',
                        data: total_active,
                        borderColor: '#776bcd',
                        fill: false,
                    },
                ]);
            })
            .catch(error => console.error('Error fetching health metrics:', error));
    }

    function updateChart(labels, datasets) {
        if (healthChart) {
            healthChart.destroy(); // Clear the previous chart
        }

        const ctx = document.getElementById('health-trends-chart').getContext('2d');
        healthChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: datasets,
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: { display: true, text: 'Date' },
                    },
                    y: {
                        title: { display: true, text: 'Values' },
                    },
                },
            },
        });
    }

    // Initial fetch for the default user
    fetchHealthTrends(dropdownUserId.value);

    // Update on user selection change
    dropdownUserId.addEventListener("change", () => {
        fetchHealthTrends(dropdownUserId.value);
    });
});


// PHENOTYPE TRENDS

document.addEventListener("DOMContentLoaded", function () {
    const dropdownUserId = document.getElementById("user_id");
    if (!dropdownUserId) {
        console.error("Dropdown element with ID 'user_id' not found.");
        return;
    }

    let phenotypeChart;

    function fetchPhenotypeTrends(userId) {
        fetch(`/get_phenotype_trends/${userId}`)
            .then(response => response.json())
            .then(phenoTypeData => {
                const labels = phenoTypeData.map(item => item.month);
                const phenotype_score = phenoTypeData.map(item => item.phenotype_score);
                
                updateChart(labels, [
                    {
                        label: 'Phenotype Score',
                        data: phenotype_score,
                        borderColor: '#8bd3c7',
                        fill: false,
                    }
                    
                ]);
            })
            .catch(error => console.error('Error fetching health metrics:', error));
    }

    function updateChart(labels, datasets) {
        if (phenotypeChart) {
            phenotypeChart.destroy(); // Clear the previous chart
        }

        const ctx = document.getElementById('phenotype-trends-chart').getContext('2d');
        phenotypeChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: datasets,
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: { display: true, text: 'Month' },
                    },
                    y: {
                        title: { display: true, text: 'Values' },
                    },
                },
            },
        });
    }

    // Initial fetch for the default user
    fetchPhenotypeTrends(dropdownUserId.value);

    // Update on user selection change
    dropdownUserId.addEventListener("change", () => {
        fetchPhenotypeTrends(dropdownUserId.value);
    });
});



// src/components/PriceChart.js
import React, { useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

Chart.register(...registerables);
Chart.register(ChartDataLabels);

const PriceChart = ({ data }) => {
    const chartRef = useRef(null);
    const chartInstanceRef = useRef(null);

    useEffect(() => {
        const createChart = () => {
            if (chartRef.current) {
                const chartContext = chartRef.current.getContext('2d');

                // Ensure prices are numbers and provide default value if missing
                const prices = [
                    parseFloat(data.flipkart_price.replace(/[^\d.-]/g, '')) || 0,
                    parseFloat(data.amazon_price.replace(/[^\d.-]/g, '')) || 0,
                    parseFloat(data.croma_price.replace(/[^\d.-]/g, '')) || 0
                ];

                console.log('Parsed Prices:', prices); // Debugging log

                chartInstanceRef.current = new Chart(chartContext, {
                    type: 'bar',
                    data: {
                        labels: ['Flipkart', 'Amazon', 'Croma'],
                        datasets: [
                            {
                                label: 'Price in INR',
                                data: prices,
                                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                                hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                                barThickness: 40, // Set the bar thickness
                            },
                        ],
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            datalabels: {
                                anchor: 'end',
                                align: 'top',
                                formatter: (value) => value.toLocaleString(), // Display price with commas
                                font: {
                                    family: 'Montserrat',
                                    weight: 'bold',
                                },
                                color: 'white',
                                offset: 5, // Increase offset to avoid overlap
                            },
                        },


                        scales: {
                            x: {
                                type: 'category',
                            },
                            y: {
                                beginAtZero: true, // Ensure the y-axis starts at zero
                                ticks: {
                                    stepSize: 100,
                                    // Set step size for Y-axis ticks
                                },
                            }
                        },
                    },
                });
            }
        };

        if (chartInstanceRef.current) {
            chartInstanceRef.current.destroy();
        }

        createChart();

        return () => {
            if (chartInstanceRef.current) {
                chartInstanceRef.current.destroy();
            }
        };
    }, [data]);

    return (
        <div className="chart-container">
            <canvas ref={chartRef} />
        </div>
    );
};

export default PriceChart;

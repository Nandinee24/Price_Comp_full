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

                // Extract site names and prices from data.site_data
                const siteNames = [];
                const prices = [];

                if (data && data.site_data) {
                    data.site_data.forEach((site) => {
                        siteNames.push(site.site_name || 'Unknown Site');
                        const price = site.price || '0';
                        prices.push(parseFloat(price.replace(/[^\d.-]/g, '')) || 0);
                    });
                } else {
                    console.error('Data or site_data is not available');
                }

                // Destroy previous chart instance if it exists
                if (chartInstanceRef.current) {
                    chartInstanceRef.current.destroy();
                }

                chartInstanceRef.current = new Chart(chartContext, {
                    type: 'bar',
                    data: {
                        labels: siteNames,
                        datasets: [
                            {
                                label: 'Price in INR',
                                data: prices,
                                backgroundColor: siteNames.map((_, index) => {
                                    const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'];
                                    return colors[index % colors.length];
                                }),
                                hoverBackgroundColor: siteNames.map((_, index) => {
                                    const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'];
                                    return colors[index % colors.length];
                                }),
                                barThickness: 40,
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
                                formatter: (value) => value.toLocaleString(),
                                font: {
                                    family: 'Montserrat',
                                    weight: 'bold',
                                },
                                color: 'white',
                                offset: 5,
                            },
                        },
                        scales: {
                            x: {
                                type: 'category',
                                ticks: {
                                    autoSkip: false, // Ensure all labels are shown
                                },
                            },
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    stepSize: 100,
                                },
                            }
                        },
                    },
                });
            }
        };

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

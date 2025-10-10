<script lang="ts">
	import { onMount } from 'svelte';
	import { Chart } from 'chart.js/auto';
	import { theme } from '$lib/stores/theme';

	let canvas: HTMLCanvasElement;
	let chart: Chart | null = null;
	export let labels: Array<string>;
	export let datasets: Array<{ label: string; data: Array<number>; backgroundColor: string }>;

	const options = {
		type: 'bar',
		data: datasets,
		options: {
			plugins: {
				legend: {
					display: false
				},
				title: {
					display: true,
					text: 'Mediciones'
				},
				tooltip: {
					callbacks: {
						label: function (context: any) {
							let label = context.dataset.label || '';
							if (label) {
								label += ': ';
							}
							label += context.parsed.y.toFixed(2);
							return label;
						}
					}
				}
			}
		},
		responsive: true,
		maintainAspectRatio: false,
		scales: {
			x: {
				stacked: true,
				beginAtZero: true,
				min: 0
			},
			y: {
				stacked: true,
				ticks: {
					stepSize: 1
				},
				min: 0
			}
		}
	};

	onMount(() => {
		const data = {
			labels: labels,
			datasets: datasets
		};
		chart = new Chart(canvas, {
			type: 'bar',
			data: data,
			options
		});
	});
</script>

<div class="relative h-[45dvh] w-full {$theme === 'dark' ? 'bg-[#2b2b2b]' : ''} p-2">
	<canvas bind:this={canvas}></canvas>
</div>

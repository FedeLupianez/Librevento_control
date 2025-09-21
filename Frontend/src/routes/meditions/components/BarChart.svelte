<script lang="ts">
	import { onMount } from 'svelte';
	import { Chart } from 'chart.js/auto';
	import { theme } from '../../../stores/theme';

	let canvas: HTMLCanvasElement;
	let chart: Chart | null = null;
	export let labels: Array<string>;
	export let prom: Array<number>;
	export let min: Array<number>;
	export let max: Array<number>;
	export let backgroundColorFunction: Function;

	const options = {
		responsive: true,
		maintainAspectRatio: false,
		scales: {
			y: {
				beginAtZero: true,
				min: 0,
				max: Math.max(...prom) + 1,
				ticks: {
					stepSize: 1
				}
			},
			x: {
				beginAtZero: true,
				min: 0,
				max: prom.length < 7 ? 7 : prom.length + 1
			}
		},
		plugins: {
			legend: {
				display: false
			},
			tooltip: {
				callbacks: {
					label: function (context: any) {
						const index = context.dataIndex;
						const prom_number = prom[index];
						const min_number = min[index];
						const max_number = max[index];
						return [
							`Promedio: ${prom_number.toFixed(2)} V`,
							`Mínimo: ${min_number.toFixed(2)} V`,
							`Máximo: ${max_number.toFixed(2)} V`
						];
					}
				}
			}
		}
	};

	onMount(() => {
		prom = [...prom, ...Array(7 - prom.length).fill(0)];
		const dataSet = {
			labels: labels,
			datasets: [
				{
					data: prom,
					backgroundColor: (ctx: any) => {
						const value = ctx.dataset.data[ctx.dataIndex];
						return backgroundColorFunction(value);
					},
					borderRadius: 5
				}
			]
		};

		chart = new Chart(canvas, {
			type: 'bar',
			data: dataSet,
			options
		});

		return () => {
			chart?.destroy(); // Limpia el gráfico al desmontar el componente
		};
	});
</script>

<div class="relative h-[45dvh] w-full {$theme === 'dark' ? 'bg-[#2b2b2b]' : ''} p-2">
	<canvas bind:this={canvas}></canvas>
</div>

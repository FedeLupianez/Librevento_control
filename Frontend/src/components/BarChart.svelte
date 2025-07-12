<script lang="ts">
	import { onMount } from 'svelte';
	import { Chart } from 'chart.js/auto';

	let canvas: HTMLCanvasElement;
	let chart: Chart | null = null;
	export let data: Array<number>;
	export let backgroundColorFunction: Function;

	const options = {
		responsive: true,
		maintainAspectRatio: false,
		scales: {
			y: {
				beginAtZero: true,
				min: 0,
				max: 12,
				ticks: {
					stepSize: 1
				}
			}
		}
	};

	onMount(() => {
		data = [...data, ...Array(7 - data.length).fill(0)];
		const dataSet = {
			labels: ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'],
			datasets: [
				{
					label: 'Voltaje Generado',
					data: data,
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

<div class="chart-container">
	<canvas bind:this={canvas}></canvas>
</div>

<style>
	.chart-container {
		position: relative;
		height: 300px;
		width: 500px;
	}
</style>

<script lang="ts">
    import { onMount } from 'svelte';
    import { Chart } from 'chart.js/auto';

    let canvas: HTMLCanvasElement;
    let chart: Chart | null = null;

    const data = {
        labels: ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'],
        datasets: [
            {
                label: 'Voltaje Generado',
                data: [8, 5, 3, 12],
                backgroundColor: (ctx: any) => {
                    const value = ctx.dataset.data[ctx.dataIndex];
                    if (value >= 8)
                        return '#789262';
                    if (value >= 5 && value < 8)
                        return '#ebdaa8';
                    if (value < 5)
                        return '#c85d4d';
                },
                borderRadius: 5
            }
        ]
    }

    const options = {
        responsive: true,
		maintainAspectRatio: false
    }

	onMount(() => {
		chart = new Chart(canvas, {
			type: 'bar',
			data: data,
			options
		});
		console.log(chart);

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
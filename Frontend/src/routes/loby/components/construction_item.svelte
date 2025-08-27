<script lang="ts">
	export let title: string;
	export let image_url: string | null;
	export let text: string | null;
</script>

{#if image_url !== null}
	<div class="flex flex-row justify-between gap-5">
		<div class="flex flex-col gap-5 px-5">
			<span class="title text-3xl">{title}</span>
			<p class="paragraph">{text}</p>
		</div>
		<img src={image_url} alt={title} class="h-auto" />
	</div>
{:else}
	<div class="flex flex-col items-start justify-start">
		<span class="title text-3xl">{title}</span>
		{#if text}
			<p class="paragraph">
				Para elevar el voltaje de la energía generada por los motores a un nivel apto para el uso.
			</p>
		{/if}
	</div>
{/if}

<style>
	.title {
		font-family: 'Gruppo';
	}
	.paragraph {
		font-family: 'Hammersmith One';
	}
</style>

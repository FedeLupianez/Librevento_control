<script lang="ts">
	export let title: string;
	export let image_url: string | null;
	export let text: string | null;
	import { theme } from '../../$lib/stores/theme';
	$: text_color = $theme === 'dark' ? 'text-white' : 'text-black';
</script>

{#if image_url !== null}
	<div class="flex flex-row justify-between gap-5">
		<div class="flex flex-col gap-5 px-5">
			<span class="title text-3xl {text_color}">{title}</span>
			<p class="paragraph {text_color}">{text}</p>
		</div>
		<img src={image_url} alt={title} class="h-auto w-1/5 object-cover object-center" />
	</div>
{:else}
	<div class="flex flex-col items-start justify-start">
		<span class="title text-3xl {text_color}">{title}</span>
		{#if text}
			<p class="paragraph {text_color}">
				{text}
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

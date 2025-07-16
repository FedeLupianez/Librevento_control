<script lang="ts">
	export let text: string;
	export let mode: string;

	let view_menu: boolean = false;
	import flechita from '/public/flechita.svg';
	function toggle() {
		view_menu = !view_menu;
	}
</script>

{#if mode === 'button'}
	<div class="relative">
		<button
			class="flex cursor-pointer items-center gap-1 font-bold text-[#2f3e2f]"
			on:click={() => toggle()}
		>
			{text}
			<img src={flechita} alt="flechita" class="-top-0.4 relative h-3.5 w-3.5" />
		</button>

		{#if view_menu}
			<div class="absolute -top-1 -left-2.5 z-10 flex flex-col rounded-md bg-[#b9c3c8] px-3 py-1">
				<button
					class="flex cursor-pointer items-center gap-1 font-bold text-[#2f3e2f]"
					on:click={() => toggle()}
				>
					{text}
					<img src={flechita} alt="flechita" class="-top-0.4 relative h-3.5 w-3.5" />
				</button>
				<slot name="menu"></slot>
			</div>
		{/if}
	</div>
{:else if mode === 'hover'}
	<div class="group relative">
		<button
			class="flex cursor-pointer items-center gap-1 font-bold text-[#2f3e2f]"
			on:click={() => toggle()}
		>
			{text}
			<img src={flechita} alt="flechita" class="-top-0.4 relative h-3.5 w-3.5" />
		</button>

		<div
			class="absolute -top-1 -left-2.5 z-10 hidden flex-col rounded-md bg-[#b9c3c8] px-3 py-1 group-hover:flex"
		>
			<button
				class="flex cursor-pointer items-center gap-1 font-bold text-[#2f3e2f]"
				on:click={() => toggle()}
			>
				{text}
				<img src={flechita} alt="flechita" class="-top-0.4 relative h-3.5 w-3.5" />
			</button>
			<slot name="menu"></slot>
		</div>
	</div>
{/if}

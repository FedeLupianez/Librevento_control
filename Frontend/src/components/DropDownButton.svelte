<script lang="ts">
	export let text: string;
	export let mode: string;

	let view_menu: boolean = false;
	function toggle() {
		view_menu = !view_menu;
	}
</script>

<div class={`group relative ${view_menu ? 'z-30' : ''}`}>
	<button
		class="relative z-20 flex cursor-pointer items-center gap-1 font-bold text-[#2f3e2f]"
		on:click={() => toggle()}
		on:mouseenter={() => {
			if (mode == 'hover') view_menu = true;
		}}
		on:mouseleave={() => {
			if (mode == 'hover') view_menu = false;
		}}
	>
		{text}
		<img src="/public/images/flechita.svg" alt="flechita" class="-top-0.4 relative h-3.5 w-3.5" />
	</button>

	{#if mode == 'button'}
		{#if view_menu}
			<div class="absolute -top-1 -left-2.5 z-10 flex flex-col rounded-md bg-[#b9c3c8] px-3 py-1">
				<div class="h-5 w-5"></div>
				<slot name="menu"></slot>
			</div>
		{/if}
	{:else}
		<div
			aria-hidden="true"
			class="absolute -top-1 -left-2.5 z-10 hidden flex-col rounded-md bg-[#b9c3c8] px-3 py-1 group-hover:flex"
			on:mouseenter={() => {
				view_menu = true;
			}}
			on:mouseleave={() => {
				view_menu = false;
			}}
		>
			<div class="h-5 w-5"></div>
			<slot name="menu"></slot>
		</div>
	{/if}
</div>

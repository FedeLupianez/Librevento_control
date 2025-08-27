<script lang="ts">
	import Icon from '@iconify/svelte';

	export let icon_name: string;
</script>

<Icon icon={icon_name} class="h-7 w-7 hover:cursor-pointer" />

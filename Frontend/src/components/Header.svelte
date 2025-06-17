<script lang="ts">
    import type { User } from "../types/user"
    import Icon from "@iconify/svelte";
    export let user: User;

</script>

<div class="container justify-between flex flex-row items-center p-5 border-b-1 border-b-[#2f3e2f]">
    {#if user.sex == "hombre"}
        <h1 class="items-center text-center">
            <span class="text-[#2f3e2f]">Bienvenido,</span> <span class="text-[#c2b280]">{user.name}</span>
        </h1>
    {:else}
        <h1 class="items-center text-center">
            <span class="text-[#2f3e2f]">Bienvenida,</span> <span class="text-[#c2b280]">{user.name}</span>
        </h1>
    {/if}

    <button class="cursor-pointer flex flex-row items-center justify-center gap-1.5 font-bold">
        Principal
        <Icon icon="bx:leaf" class="w-5 h-5"/>
    </button>
    <button class="cursor-pointer flex flex-row items-center justify-center gap-1.5 font-bold">
        Estadísticas
        <Icon icon="ep:arrow-down-bold" class="w-4 h-4 text-center items-center"/>
    </button>
    <button class="cursor-pointer flex flex-row items-center justify-center gap-1.5 font-bold">
        Editar
        <Icon icon="ep:arrow-down-bold" class="w-4 h-4 text-center items-center"/>
    </button>

    <button class="cursor-pointer">
        <img src={user.imageUrl} alt="Foto de perfil" class="rounded-full h-15 w-15">
    </button>
</div>
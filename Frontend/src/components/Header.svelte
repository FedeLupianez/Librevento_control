

<script lang="ts">
    import type { User } from "../types/user"
    import Icon from "@iconify/svelte";
    import flechita from '/public/flechita.svg';
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

    <div class="flex gap-x-30 text-lg">
        <button class="cursor-pointer flex flex-row items-center justify-center gap-1.5 font-bold">
            principal
            <Icon icon="bx:leaf" class="w-5 h-5"/>
        </button>
        <button class="cursor-pointer flex flex-row items-center justify-center gap-1 font-bold">
            estadísticas
            <img src={flechita} alt="flechita" class="w-3.5 h-3.5 relative -top-0.4"  />
        </button>
        <button class="cursor-pointer flex flex-row items-center justify-center gap-1 font-bold">
            editar
            <img src={flechita} alt="flechita" class="w-3.5 h-3.5 relative -top-0.4"  />
        </button>
    </div>
    
    <button class="cursor-pointer">
        <img src={user.imageUrl} alt="Foto de perfil" class="rounded-full h-10 w-10">
    </button>
</div>


<script lang="ts">
    import type { User } from "../types/user"
    import Icon from "@iconify/svelte";
    import flechita from '/public/flechita.svg';
    export let user: User;
    
</script>

<div class="container justify-between flex flex-row items-center py-5 px-15 border-b-0 border-b-[#2f3e2f]">
    {#if user.sex == "hombre"}
        <h1 class="items-center text-center mr-15">
            <span class="text-[#2f3e2f]">Bienvenido,</span> <span class="text-[#c2b280]">{user.name}</span>
        </h1>
    {:else}
        <h1 class="items-center text-center">
            <span class="text-[#2f3e2f]">Bienvenida,</span> <span class="text-[#c2b280]">{user.name}</span>
        </h1>
    {/if}

    <div class="flex gap-x-20 text-lg">
        <button class="cursor-pointer flex flex-row items-center justify-center gap-1.5 font-bold">
            principal
            <Icon icon="bx:leaf" class="w-5 h-5"/>
        </button>
        <div class="relative group"> <!-- se hace una familia uwu de los div adentro -->
            <button class="cursor-pointer flex items-center font-bold text-[#2f3e2f] gap-1">
                estadísticas
                <img src={flechita} alt="flechita" class="w-3.5 h-3.5 relative -top-0.4"  />
            </button>

            <!-- pestaña gris -->
            <div class="absolute -top-1 left-0 hidden group-hover:block bg-[#b9c3c8] rounded-md px-3 py-1 z-10">
                <span class="font-bold text-[#2f3e2f]">estadísticas</span>
            </div>

            <!-- Menú desplegable -->
            <div class="absolute left-0 mt-1 hidden group-hover:flex flex-col bg-[#7A9660] rounded-md shadow-md w-52 z-20">
                <a href="/consumo-dia" class="px-4 py-2 text-white font-bold hover:bg-[#6b8755] rounded-t-md">Consumo por día</a>
                <a href="/consumo-mes" class="px-4 py-2 text-white font-bold hover:bg-[#6b8755]">Consumo por mes</a>
                <a href="/alertas" class="px-4 py-2 text-white font-bold hover:bg-[#6b8755] rounded-b-md">Alertas de consumo</a>
            </div>
        </div>
        <button class="cursor-pointer flex flex-row items-center justify-center gap-1 font-bold">
            editar
            <img src={flechita} alt="flechita" class="w-3.5 h-3.5 relative -top-0.4"  />
        </button>
    </div>
    
    <button class="cursor-pointer">
        <img src={user.imageUrl} alt="Foto de perfil" class="rounded-full h-10 w-10">
    </button>

</div>

<div class="w-228 h-0.5 bg-gray-500"></div>

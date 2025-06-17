<script lang="ts">
    import type { User } from "../types/user"
    export let user: User;

</script>

<div class="container justify-between flex flex-row items-center p-5 border-b-1 border-b-[#2f3e2f]">
    {#if user.sex == "hombre"}
        <h1 class="items-center text-center ">
            <span class="text-[#2f3e2f]">Bienvenido,</span> <span class="text-[#c2b280]">{user.name}</span>
        </h1>
    {:else}
            <span class="text-[#2f3e2f]">Bienvenida,</span> <span class="text-[#c2b280]">{user.name}</span>
    {/if}

    <button class="cursor-pointer">Principal</button>
    <button class="cursor-pointer">Estadísticas</button>
    <button class="cursor-pointer">Editar</button>

    <button class="cursor-pointer">
        <img src={user.imageUrl} alt="Foto de perfil" class="rounded-full h-15 w-15">
    </button>
</div>
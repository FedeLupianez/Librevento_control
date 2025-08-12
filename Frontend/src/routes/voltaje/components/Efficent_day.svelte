<script lang='ts'>
    export let date: string;
    let day_name = new Date(date).getDay();
    console.log(day_name);
</script>

<div class="flex items-center gap-2">
    <p>El día mas eficiente de la semana fué el</p>
    <span>{day_name}</span>
    <img src="/public/images/hojas.svg" alt="Hojita">
</div>
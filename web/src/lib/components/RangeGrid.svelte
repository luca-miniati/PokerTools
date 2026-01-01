<script lang="ts">
    import RangeCell from './RangeCell.svelte';
    import { RANKS } from '$lib/utils/range';
    import type { Range } from '$lib/utils/range';

    export let range: Range;
</script>

<div class="grid">
    {#each RANKS as row}
        {#each RANKS as col}
            <RangeCell
                {row}
                {col}
                {range}
            />
        {/each}
    {/each}
</div>

<style>
    .grid {
        display: grid;
        width: 100%;
        height: 100%;
        grid-template-rows: repeat(13, calc((100% - (13 - 1) * 2px) / 13));
        grid-template-columns: repeat(13, calc((100% - (13 - 1) * 2px) / 13));
        gap: 2px;
    }
</style>

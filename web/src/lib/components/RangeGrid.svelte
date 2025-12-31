<script lang="ts">
    import RangeCell from './RangeCell.svelte';
    import { RANKS } from '$lib/utils/range';
    import type { PokerRange } from '$lib/utils/range';

    export let range: PokerRange;
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
        grid-template-columns: repeat(13, 1fr);
        grid-template-rows: repeat(13, 1fr);
        gap: 14px;
    }
</style>

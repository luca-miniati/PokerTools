<script lang="ts">
    import RangeCell from './RangeCell.svelte';
    import { RANKS } from '$lib/utils/range';
    import type { Range } from '$lib/utils/range';
    import { selectedRange } from '$lib/stores/rangeStore';
</script>

{#if $selectedRange}
    <div class="grid">
        {#each RANKS as row}
            {#each RANKS as col}
                <RangeCell
                    {row}
                    {col}
                    range={$selectedRange}
                />
            {/each}
        {/each}
    </div>
{:else}
    <div>Select a range</div>
{/if}

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

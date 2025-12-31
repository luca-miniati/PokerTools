<script lang="ts">
    import { PokerRange } from '$lib/utils/range';
    import RangeGrid from '$lib/components/RangeGrid.svelte';
    import RangeTree from '$lib/components/RangeTree.svelte';
    import RangeInfo from '$lib/components/RangeInfo.svelte';
    import { rangeTree } from '$lib/components/rangeTree'
    import { selectedRange } from '$lib/stores/rangeStore'

</script>

<main>
    <div class="range-grid-info">
        <div class="range-info">
            <RangeInfo />
        </div>
        <div class="range-grid">
            {#if $selectedRange}
                <RangeGrid range={$selectedRange} />
            {/if}
        </div>
    </div>
    <div class="range-tree">
        <RangeTree nodes={rangeTree}/>
    </div>
</main>

<style>
    main {
        padding: 30px;
        display: flex;
        flex-direction: row;
        box-sizing: border-box;
        height: 100vh;
    }

    .range-grid-info {
        flex: 0 0 80%;
    }

    .range-info {
        height: 5%;
    }

    .range-grid {
        height: 95%;
    }

    .range-tree {
        flex: 0 0 20%;
        overflow: scroll;
    }
</style>

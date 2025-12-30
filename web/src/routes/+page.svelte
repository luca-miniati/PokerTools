<script lang="ts">
    import { Range } from '$lib/utils/range';
    import RangeGrid from '$lib/components/RangeGrid.svelte';
    import RangeTree from '$lib/components/RangeTree.svelte';
    import { rangeTree } from '$lib/components/rangeTree'
    import { selectedRange } from '$lib/stores/rangeStore'

</script>

<main>
    <div class="range-grid">
        <RangeGrid {$selectedRange} />
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

    .range-grid {
        flex: 0 0 80%;
        min-width: 0;
    }

    .range-tree {
        flex: 0 0 20%;
        min-width: 0;
        overflow: scroll;
    }
</style>

<script lang="ts">
  import { selectedRange } from '$lib/stores/rangeStore';
  import RangeGrid from '$lib/components/RangeGrid.svelte';
  import RangeTree from '$lib/components/RangeTree.svelte';
  import RangeInfo from '$lib/components/RangeInfo.svelte';
  import { rangeTree } from '$lib/components/rangeTree';
  import Navbar from '$lib/components/Navbar.svelte';
</script>


<main class="app">
    <Navbar />
    <section class="range-grid-info">
        <RangeInfo />
        {#if $selectedRange}
            <div class="range-grid">
                <RangeGrid range={$selectedRange} />
            </div>
        {/if}
    </section>

    <aside class="range-tree">
        <RangeTree nodes={rangeTree} />
    </aside>
</main>

<style>
*,
*::before,
*::after {
  box-sizing: border-box;
}

html,
body {
  height: 100%;
  margin: 0;
}

.app {
  display: flex;
  height: 100vh;
}

.range-grid-info {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    min-width: 0;
    margin-top: 1.0rem;
    margin-left: var(--nav-collapsed);
    padding-left: 1.0rem;
}

.range-grid {
    flex: 1 1 auto;
}

.range-tree {
    flex: 0 0 15%;
    padding-top: 1.0rem;
    border-left: 1px solid var(--navbar-border);
}
</style>

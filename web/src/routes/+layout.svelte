<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
    import 'typeface-fira-code';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<style>
    :global(:root) {
		--bg: #191724;
		--bg-muted: #1f1d2e;
		--bg-navbar: #1a1a1f;
		--navbar-border: #2a2a2f;
		--navbar-item: #2f2f3a;
		--fg: #e0def4;
		--fg-muted: #6e6a86;
		--primary: #eb6f92;
		--secondary: #9ccfd8;
		--accent: #c4a7e7;
		--border: #332e4d;
        --call: #333a3a;
        --raise: #575279;
        --allin: #894f60;
		--nav-collapsed: 3.0rem;
		--nav-expanded: 12.0rem;
		--tree-width: 10vw;
		--gap: 2rem;
	}

    :global(body) {
		font-family: 'Fira Code', monospace;
		background-color: var(--bg);
		color: var(--fg);
		margin: 0;
		padding: 0;
	}

	:global(a) {
		color: var(--primary);
		text-decoration: none;
	}

</style>

{@render children()}

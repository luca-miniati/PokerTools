<script>
    const navItems = [
        { icon: "pt", label: "pokertools", href: "/" },
        { icon: "rv", label: "range viewer", href: "/range-viewer" },
    ];
</script>

<nav class="sidebar">
    {#each navItems as item}
        <a class="nav-item" href={item.href}>
            <span class="icon">{item.icon}</span>
            <span class="label">{item.label}</span>
        </a>
    {/each}
</nav>

<style>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;

  width: var(--nav-collapsed);
  background: var(--bg-navbar);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  border-right: 1px solid var(--navbar-border);

  transition: width 0.25s ease;
  z-index: 100;
  overflow: hidden;
}

.sidebar:hover {
  width: var(--nav-expanded);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;

  text-decoration: none;
  padding: 0.6rem;
  white-space: nowrap;

  transition: background 0.2s ease;
}

.nav-item:hover {
  background: var(--navbar-item);
}

.icon {
  font-size: 1.25rem;
  text-align: center;
}

.label {
  opacity: 0;
  transition: opacity 0.2s ease;
  color: var(--fg);
}

.sidebar:hover .label {
  opacity: 1;
}
</style>
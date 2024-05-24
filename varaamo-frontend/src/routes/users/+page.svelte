<script lang="ts">
    import { PageData } from './$types';

    export let users;
</script>

<ul>
    {#each users as user}
        <li>{user.name}, {user.group}</li>
    {/each}
</ul>

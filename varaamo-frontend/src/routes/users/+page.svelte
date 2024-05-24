<script lang="ts">
    export let data;
</script>

<ul>
    {#each data.allUsers as user}
        <li>{user.name}, {user.users_rentalusergroup.name}</li>
    {/each}
</ul>

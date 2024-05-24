<script lang="ts">
    export let data;
</script>

<ul class="list">
    {#each data.allUsers as user}
        <li>{user.name}, {user.users_rentalusergroup.name}</li>
    {/each}
</ul>

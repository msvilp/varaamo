import prisma from '$lib/prisma';
import type { PageServerLoad } from './$types';

export const load = (async () => {
    const users = await prisma.users_rentaluser.findMany({
        include: {
            users_rentalusergroup: true
        }
    });

    return { allUsers: users };
}) satisfies PageServerLoad;
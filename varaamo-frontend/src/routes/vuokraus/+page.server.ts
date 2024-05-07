import prisma from '$lib/prisma';
import type { PageServerLoad } from './$types';

export const load = (async () => {
    const classItems = await prisma.equipment_equipmentitem.findMany({
        include: {
            equipment_equipmentclass: true
        }
    });

    return { feed: classItems };
}) satisfies PageServerLoad;
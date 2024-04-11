import prisma from '$lib/prisma';
import type { PageServerLoad } from './$types';

export const load = (async () => {
  // Load data from database
  const response = await prisma.equipment_equipmentitem.findMany()

  // Return data to the page.svelte
  return { feed: response };
}) satisfies PageServerLoad;
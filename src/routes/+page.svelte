<script lang="ts">
  import { SvelteMap } from "svelte/reactivity";
  import type { ChangeEventHandler } from "svelte/elements";
  import { enhance } from "$app/forms";
  import type { ActionData, PageData } from "./$types";

  let { data, form }: { data: PageData; form: ActionData } = $props();

  let type = $state<string>();
  let genresMap = new SvelteMap<string, string[]>();
  let genres = $derived(genresMap.get(type ?? "") ?? []);
  let genre = $state<string>();
  let score = $state<string>();

  $inspect(genresMap);

  const onTypeChange: ChangeEventHandler<HTMLSelectElement> = (event) => {
    const { value } = event.target as HTMLSelectElement;
    genre = "";
    if (!genresMap.has(value)) {
      fetch("/api/genres?type=" + value).then((resp) => {
        resp.json().then((data) => {
          console.log(data);
          genresMap.set(value, data.genres);
        });
      });
    }
  };
</script>

<div class="min-h-svh flex items-center justify-center">
  <div
    class="m-5 w-full max-w-lg border border-neutral-200 border-dashed p-5 rounded-xl"
  >
    <h1 class="text-3xl text-center mb-5">随便看点</h1>

    <form class="space-y-5" method="POST" use:enhance>
      <div class="flex flex-col gap-2">
        <label for="type">选择类型</label>
        <select
          bind:value={type}
          required
          name="type"
          id="type"
          class="border h-10 px-2 focus-within:outline-none rounded border-neutral-200 w-full"
          onchange={onTypeChange}
        >
          <option value="">请选择</option>
          {#each data.types as item}
            <option value={item}>{item}</option>
          {/each}
        </select>
      </div>

      <div class="flex flex-col gap-2">
        <label for="genre">选择标签</label>
        <select
          bind:value={genre}
          required
          name="genre"
          id="genre"
          class="border h-10 px-2 focus-within:outline-none rounded border-neutral-200 w-full"
        >
          <option value="">请选择</option>
          {#each genres as item}
            <option value={item}>{item}</option>
          {/each}
        </select>
      </div>

      <div class="flex flex-col gap-2">
        <label for="score">最低评分</label>
        <input
          bind:value={score}
          required
          type="number"
          name="score"
          id="score"
          placeholder="请输入最低评分"
          min="0"
          step="0.1"
          class="h-10 px-2 border border-neutral-200 focus-within:outline-none rounded w-full"
        />
      </div>

      <button
        type="submit"
        class="h-10 w-full group px-4 py-1 rounded-lg font-medium bg-linear-to-b from-neutral-800 to-neutral-900 text-neutral-50 shadow-md shadow-black/15 border border-neutral-950 inset-shadow-[0_1px_0px_0px] inset-shadow-white/70 active:inset-shadow-none transition"
      >
        <span class="block transform-3d group-active:translate-y-px">
          随便看看
        </span>
      </button>
    </form>

    <div
      class="p-4 min-h-20 bg-neutral-100 rounded mt-5 flex items-center justify-center"
    >
      {#if form?.success}
        <p>
          <span class="font-semibold">{form.data.type}：</span>《{form.data
            .name}》
        </p>
      {/if}
      {#if form?.missing}
        <p class="text-red-500">没有符合条件的项目</p>
      {/if}
    </div>
  </div>
</div>

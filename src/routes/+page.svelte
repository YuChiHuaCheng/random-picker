<script lang="ts">
  import { SvelteMap } from "svelte/reactivity";
  import { superForm } from "sveltekit-superforms";
  import { zodClient } from "sveltekit-superforms/adapters";
  import { Field, Control, Label } from "formsnap";
  import { Check, Clipboard, Loader } from "lucide-svelte";
  import { copyText } from "svelte-copy";
  import type { PageData } from "./$types";
  import { schema } from "./schema";
  import type { Resource } from "$lib/server/helper";

  const { data }: { data: PageData } = $props();

  let resource = $state<Resource | null | undefined>();
  let loading = $state(false);
  let copied = $state(false);

  const form = superForm(data.form, {
    validators: zodClient(schema),
    resetForm: false,
    onResult: ({ result }) => {
      loading = false;
      if (result.type === "success" && result.data) {
        const form = result.data["form"];
        const random = form.message.random as [Resource];
        resource = random ? random[0] : null;
      }
    },
    onSubmit: () => {
      loading = true;
    },
  });
  const { form: formData, enhance } = form;

  const genreMap = new SvelteMap<string, string[]>();
  const genres = $derived.by(() => {
    if ($formData.type) {
      return genreMap.get($formData.type) || [];
    }
    return [];
  });

  const onTypeChange = (event: Event) => {
    $formData.genre = "";
    const target = event.target as HTMLSelectElement;
    const value = target.value;
    if (value && !genreMap.has(value)) {
      fetch("/api/genres?type=" + value).then((resp) => {
        resp.json().then((data) => {
          genreMap.set(value, data.genres);
        });
      });
    }
  };
</script>

<main class="min-h-svh flex justify-center p-5">
  <div
    class="max-w-lg w-full border border-dashed border-neutral-300 rounded-lg p-5"
  >
    <h1 class="text-center text-3xl">随便看点</h1>

    <form method="POST" use:enhance class="mt-5 space-y-5">
      <div>
        <Field {form} name="type">
          <Control>
            {#snippet children({ props })}
              <Label class="block mb-1 text-neutral-500">选择类型</Label>
              <select
                class="w-full h-10 border px-2 rounded-md border-neutral-200"
                {...props}
                bind:value={$formData.type}
                onchange={onTypeChange}
              >
                <option value="">请选择</option>
                {#each data.types as item}
                  <option value={item}>{item}</option>
                {/each}
              </select>
            {/snippet}
          </Control>
        </Field>
      </div>

      <div>
        <Field {form} name="genre">
          <Control>
            {#snippet children({ props })}
              <Label class="block mb-1 text-neutral-500">选择标签</Label>
              <select
                class="w-full h-10 border px-2 rounded-md border-neutral-200"
                {...props}
                bind:value={$formData.genre}
              >
                <option value="">请选择</option>
                {#each genres as item}
                  <option value={item}>{item}</option>
                {/each}
              </select>
            {/snippet}
          </Control>
        </Field>
      </div>

      <div>
        <Field {form} name="score">
          <Control>
            {#snippet children({ props })}
              <Label class="block mb-1 text-neutral-500"
                >最低评分(范围0-5)</Label
              >
              <input
                type="number"
                {...props}
                required
                placeholder="请输入最低评分"
                bind:value={$formData.score}
                min="0"
                max="5"
                step="0.1"
                class="h-10 px-2 border border-neutral-200 rounded-md w-full"
              />
            {/snippet}
          </Control>
        </Field>
      </div>

      <button
        disabled={loading}
        type="submit"
        class={[
          "h-10 w-full px-4 rounded-md font-medium group",
          "flex items-center justify-center",
          "transition bg-blue-500 text-blue-50",
          "inset-shadow-sm inset-shadow-white/20 ring ring-blue-600 inset-ring inset-ring-white/15",
        ]}
      >
        {#if loading}
          <Loader class="size-5 animate-spin" />
        {:else}
          <span class="block transform-3d group-active:translate-y-px">
            随便看看
          </span>
        {/if}
      </button>
    </form>

    {#if resource !== undefined}
      <div class="p-10 mt-5 min-h-24 rounded-md bg-neutral-100 relative">
        {#if resource === null}
          <p class="text-center text-neutral-500">没有找到符合条件的资源</p>
        {:else}
          <h3 class="text-center text-neutral-500">{resource.Type}</h3>
          <p class="text-center">《{resource.Item_name}》</p>

          <button
            class="absolute right-2 top-2"
            onclick={() => {
              copyText(resource!.Item_name);
              copied = true;
              setTimeout(() => {
                copied = false;
              }, 2000);
            }}
          >
            {#if copied}
              <Check class="size-5 text-green-500" />
            {:else}
              <Clipboard class="size-5 text-neutral-500" />
            {/if}
          </button>
        {/if}
      </div>
    {/if}
  </div>
</main>

<script>
import { createEventDispatcher } from 'svelte'

const dispatch = createEventDispatcher()

// dom elements to manipulate
let textInput

let isEditing

export let itemId
export let content
export let isComplete

function deleteItem () {
  dispatch('deleteItem', {itemId: itemId})
}

function showEdit () {
  isEditing = true
}

async function submit (e) {
  if (e.keyCode === 13) {
    editItem()
    textInput.blur()
  }
}

function editItem () {
  const ev = {
    itemId: itemId,
    content: content,
    isComplete: isComplete
  }
  dispatch('itemUpdate', ev)
  isEditing = false
}
</script>

<li class="field is-grouped todo-list-item" class:complete="{isComplete}">
    <input type="hidden" bind:value={itemId} />
    <p class="control checkbox">
        <input type="checkbox" bind:checked={isComplete} on:change={editItem} />
    </p>
    <p class="control is-expanded">
      <input class="input content"
        bind:this={textInput}
        on:click={showEdit}
        on:keyup={submit}
        on:blur={editItem}
        class:is-static="{!isEditing}" 
        class:complete="{isComplete}" 
        bind:value={content} />
    </p>
    <p class="control">
      <button class="button" on:mousedown={deleteItem} class:hidden="{!isEditing}">delete</button>
    </p>
</li>

<style scoped>
.complete .is-static {
  color: #999;
  text-decoration: line-through;
}
.hidden {
  display: none;
}
input[type=checkbox]{
  vertical-align: middle;
  height: 100%;
}
</style>

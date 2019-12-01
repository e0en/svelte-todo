<script>
import TodoItem from './TodoItem.svelte'
import Login from './Login.svelte'
import { backendUrl } from '../settings.js'
import { createEventDispatcher, onMount } from 'svelte'
import axios from 'axios'

axios.defaults.withCredentials = true

let newContent = ''
let items = []
let hideCompleted = false
let isLoggedIn = true


function getAll () {
  axios.get(backendUrl + '/todo')
    .then((res) => {
      isLoggedIn = true
      items = []
      res.data.forEach(d => items.push(d))
    })
    .catch(() => {
      isLoggedIn = false
    })
}

function update (ev) {
  items.forEach(function (item) {
    if (item.itemId === ev.detail.itemId) {
      item.isComplete = ev.detail.isComplete
      item.content = ev.detail.content
      axios.put(backendUrl + '/todo/' + item.itemId, item)
        .then(() => {
        })
    }
  })
}

function addNewItem (ev) {
  var newId = items.length.toString()
  const newItem = { itemId: newId, content: newContent, isComplete: false }
  axios.post(backendUrl + '/todo', newItem)
    .then(() => {
        items.push(newItem)
        return false
    })

  newContent = ''
  return false
}

function deleteItem (ev) {
  axios.delete(backendUrl + '/todo/' + ev.detail.itemId)
    .then(() => {
      items = items.filter(function (item) {
        return item.itemId !== ev.detail.itemId
      })
    })
}

function toggleHideCompleted () {
  hideCompleted = !hideCompleted
}

function handleLogin (isSuccess) {
  if (isSuccess) {
    isLoggedIn = true
    getAll()
  } else {
    isLoggedIn = false
  }
}

function logout () {
  axios.get(backendUrl + '/logout')
    .then(() => {
      items = []
      isLoggedIn = false
    })
}

onMount(async () => { getAll() })

</script>

<div class="container todo-list">
  <form class="field" on:submit={addNewItem}>
    <p class="control">
      <label for="newContent">Add a new task</label><br />
      <input class="input" type="text" name="newContent" value={newContent} />
    </p>
  </form>
  <div class="field">
    <button class="button is-small" on:click={toggleHideCompleted}>{ hideCompleted ? "Show" : "Hide" } completed</button>
  </div>
  <ul>
    {#each items as item}
    {#if !(item.isComplete && hideCompleted)}
    <TodoItem 
      itemId={item.itemId} content={item.content} isComplete={item.isComplete}
      on:itemUpdate={update} on:deleteItem={deleteItem} />
    {/if}
    {/each}
  </ul>
  <div class="container" class:hidden="{!isLoggedIn}">
      <button class="button is-danger is-light" on:click={logout}>
          Logout
      </button>
  </div>
</div>
<Login isActive={!isLoggedIn} on:login={handleLogin} />

<style>
div.todo-list {
  margin: 1em auto;
  text-align: left;
}
.content ul {
  list-style-type: none;
  margin-left: 0;
  padding-left: 0;
}
.hidden {
  display: none;
}
</style>

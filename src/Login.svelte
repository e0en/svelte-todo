<script>
import { backendUrl } from '../settings.js'
import axios from 'axios'
import { createEventDispatcher } from 'svelte'

const dispatch = createEventDispatcher()

axios.defaults.withCredentials = true

export let isActive

let email
let password

function submitLogin () {
  console.log(backendUrl)
  axios.post(backendUrl + '/login', { email: email, pw: password })
    .then((res) => {
      dispatch('login', true)
      return false
    })
    .catch(() => {
      dispatch('login', false)
      return false
    })
}

</script>

<div class="modal" class:is-active="{isActive}">
    <div class="modal-background"></div>
    <div class="modal-content">
      <form class="box" action="#" on:submit={submitLogin}>
        <div class="field">
          <label class="label">Email</label>
          <div class="control">
            <input class="input" type="email" bind:value={email} />
          </div>
        </div>

        <div class="field">
          <label class="label">Password</label>
          <div class="control">
            <input class="input" type="password" bind:value={password} />
          </div>
        </div>

        <div class="field">
          <div class="control">
            <button class="button" on:click={submitLogin}>Login</button>
          </div>
        </div>

      </form>
    </div>
</div>


<style>
form {
  margin: 0 auto;
}
</style>

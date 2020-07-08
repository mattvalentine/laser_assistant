<template>
  <div class="params">
    <form action="http://localhost:5000/parameters" method="POST">
      <p>
        Thickness (mm):
        <br />
        <input name="thickness" value="3.1" />
      </p>

      <p>
        Material
        <br />
        <select name="material">
          <option disabled value>Please select one</option>
          <option>Wood</option>
          <option>Acrylic</option>
          <!-- <option>C</option> -->
        </select>
      </p>

      <p>
        Kerf Radius (mm):
        <br />
        <input name="kerf" value="0.25" />
      </p>
      <button type="submit">Apply</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "Parameters"
};
</script>

<style scoped>
.params {
  grid-column: 4 / 5;
  grid-row: 1;
  background-color: lightgrey;
  margin: 1vmin;
  border-radius: 2vmin;
}
.params > form {
  margin: 1vmin;
}
</style>
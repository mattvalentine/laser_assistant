<template>
  <div class="loader">
    <input
      class="loadbutton"
      type="file"
      id="SVGfile"
      aria-label="open svg"
      accept=".svg"
      @change="loadFile"
    />
    <div class="buttonholder" @click="passClick">
      <span class="loadlabel">Select file</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoadSVG",
  methods: {
    loadFile: async function (event) {
      const svgfile = event.target.files[0];
      const svgcontent = await new Response(svgfile).text();
      console.log(svgcontent);
      this.$emit("insvg", svgcontent);
      return;
    },
    passClick: function () {
      document.getElementById("SVGfile").click();
    },
  },
};
</script>

<style>
.loader {
  grid-row: 1;
  grid-column: 1/3;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 50;
  height: 100vh;
  text-align: center;
  background-color: white;
}

.loadbutton {
  display: none;
}
.buttonholder {
  background: lightgrey;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.6);
  /* box-shadow: 1px 1px 3px black; */
  padding: 20px;
  border-radius: 3px;
}
.buttonholder:hover,
.buttonholder:focus {
  background: darkgrey;
  cursor: pointer;
}

.loadlabel {
  font-family: sans-serif;
  font-size: 2rem;
}
</style>
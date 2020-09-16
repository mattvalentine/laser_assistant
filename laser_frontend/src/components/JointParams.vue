<template>
  <div class="jointparams" :display="show">
    <div class="jointoptions">
      <span class="paramlabel">Joint type</span>
      <select name="jointtype" v-model="jp.joint_type">
        <option disabled value>Please select one</option>
        <option>Box</option>
        <option>Tab-and-Slot</option>
        <option>Interlocking</option>
        <option>Bolt</option>
        <option>Flat</option>
        <option>Divider</option>
      </select>

      <span class="paramlabel">Joint alignment</span>
      <select name="jointalign" v-model="jp.joint_align">
        <option disabled value>Please select one</option>
        <option>Inside</option>
        <option>Middle</option>
        <option>Outside</option>
      </select>

      <span class="paramlabel" v-show="jp.joint_type!=='Bolt'">Fit</span>
      <select name="fit" v-model="jp.fit" v-show="jp.joint_type!=='Bolt'">
        <option disabled value>Please select one</option>
        <option>Clearance</option>
        <option>Friction</option>
        <option>Press</option>
      </select>

      <span
        class="paramlabel"
        v-show="jp.joint_type==='Tab-and-Slot' || jp.joint_type==='Box'"
      >Tab Size(mm)</span>
      <input
        name="tabsize"
        v-model="jp.tabsize"
        v-show="jp.joint_type==='Tab-and-Slot' || jp.joint_type==='Box'"
        type="number"
        step="1.0"
      />

      <span
        class="paramlabel"
        v-show="jp.joint_type==='Tab-and-Slot' || jp.joint_type==='Box'"
      >Tab Spacing(mm)</span>
      <input
        name="tabspace"
        v-model="jp.tabspace"
        v-show="jp.joint_type==='Tab-and-Slot' || jp.joint_type==='Box'"
        type="number"
        step="1.0"
      />

      <span
        class="paramlabel"
        v-show="jp.joint_type==='Tab-and-Slot' || jp.joint_type==='Box'"
      >Number of Tabs</span>
      <input
        name="tabnum"
        v-model="jp.tabnum"
        v-show="jp.joint_type==='Tab-and-Slot' || jp.joint_type==='Box'"
        type="number"
        step="1"
      />

      <span class="paramlabel" v-show="jp.joint_type==='Bolt'">Bolt size</span>
      <select name="boltsize" v-model="jp.boltsize" v-show="jp.joint_type==='Bolt'">
        <option disabled value>Please select one</option>
        <option>M2</option>
        <option>M2.5</option>
        <option>M3</option>
        <option>M4</option>
      </select>

      <span class="paramlabel" v-show="jp.joint_type==='Bolt'">Number of Bolts</span>
      <input
        name="boltnum"
        v-model="jp.boltnum"
        v-show="jp.joint_type==='Bolt'"
        type="number"
        step="1"
      />

      <span class="paramlabel" v-show="jp.joint_type==='Bolt'">Space between Bolts</span>
      <input
        name="boltspace"
        v-model="jp.boltspace"
        v-show="jp.joint_type==='Bolt'"
        type="number"
        step="0.1"
      />

      <span class="paramlabel" v-show="jp.joint_type==='Bolt'">Bolt Length(mm)</span>
      <input
        name="boltlength"
        v-model="jp.boltlength"
        v-show="jp.joint_type==='Bolt'"
        type="number"
        step="0.1"
      />
      <div id="flipjoint">
        <button @click="flipjoint">Reverse Joint</button>
      </div>
      <div id="applyjoint">
        <button @click="confirmjoint">Apply</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "JointParams",
  props: ["show", "setjp"],
  data: function () {
    return {
      jp: this.setjp,
    };
  },
  watch: {
    setjp: function (updatedjp) {
      this.jp = updatedjp;
    },
  },
  methods: {
    confirmjoint: function () {
      console.log("confirm");
      this.jp.tabsize = parseFloat(this.jp.tabsize);
      this.jp.tabspace = parseFloat(this.jp.tabspace);
      this.jp.tabnum = parseInt(this.jp.tabnum);
      this.jp.boltnum = parseInt(this.jp.boltnum);
      this.jp.boltspace = parseInt(this.jp.boltspace);
      this.jp.boltlength = parseInt(this.jp.boltlength);
      this.$emit("confirm", this.jp);
    },
    flipjoint: function () {
      this.$emit("flipjoint");
    },
  },
};
</script>

<style>
.jointparams {
  z-index: 20;
  grid-area: svg;
  /* background-color: red; */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.jointoptions {
  background: lightgray;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 1px 4px rgba(0, 0, 0, 0.4);
  /* cursor: pointer; */
  /* line-height: 3vmin; */
  display: grid;
  grid-template-columns: 50% 50%;
  grid-gap: 5px;
}
#applyjoint {
  grid-column: 1/3;
  display: flex;
  align-items: center;
  justify-content: center;
  /* width: 200px; */
}
#applyjoint > button {
  padding: 5px;
}
</style>
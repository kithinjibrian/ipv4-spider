<template>
  <v-container class="fill-height">
  <v-responsive class="d-flex fill-height">
    <v-data-table :headers="headers" :items="ipAddresses">
    <template v-slot:item="{ item }">
      <tr>
        <td>
          <v-checkbox></v-checkbox>
        </td>
        <td
        @click="$router.push(`/ip?ip=${item.columns.ip}`)">{{ item.columns.ip }}</td>
        <td>
          <span v-for="(port, index) in item.columns.port" :key="index">
            <v-chip>{{ port }}</v-chip>
          </span>
        </td>
        <td>
          <v-textarea
          variant="underlined"
          rows="1"
          auto-grow></v-textarea>
        </td>
      </tr>
    </template>
  </v-data-table>
  </v-responsive>
  </v-container>
</template>

<script setup>
import { useAppStore } from '@/store/app';
import {VDataTable} from "vuetify/labs/VDataTable"

const store = useAppStore()

const ipAddresses = Object.entries(store.ip).map(([ipAddress, ports]) => {
return {
ipAddress,
ports: ports.map(port => port.port)
};
});

const headers = [
{title:"Exploited"},
{ title: 'IP Address', value: 'ipAddress', key:"ip" },
{ title: 'Open Ports', value: 'ports',key:"port" },
{title:"Comments"},
]
</script>

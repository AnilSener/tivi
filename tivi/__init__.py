from tiviapp.apis import schedule_rest
seconds=7*24*60*60
schedule_rest.executeTVListingAPI.delay(seconds)
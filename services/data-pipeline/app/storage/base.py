class BaseStorage:
    async def save(self, data, metadata):
        """
        Save data to storage. Must be implemented by subclasses.
        """
        raise NotImplementedError

    async def aggregate_and_save(self, new_data, metadata):
        """
        Aggregate and save data to storage. Must be implemented by subclasses.
        """
        raise NotImplementedError

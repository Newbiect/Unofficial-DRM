class Buffer:
    def __init__(self, capacity):
        self.mRangeOffset = 0
        self.mOwnsData = True
        self.mData = bytearray(capacity)
        if self.mData is None:
            self.mCapacity = 0
            self.mRangeLength = 0
        else:
            self.mCapacity = capacity
            self.mRangeLength = capacity

    def __del__(self):
        if self.mOwnsData:
            if self.mData is not None:
                del self.mData
                self.mData = None
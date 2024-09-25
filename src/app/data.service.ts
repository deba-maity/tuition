import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private items: any[] = [
    { id: 1, name: 'John', age: 30 },
    { id: 2, name: 'Alice', age: 25 },
    // Add more data as needed
  ];

  getItems() {
    return this.items;
  }

  updateItem(updatedItem: any) {
    // Find the item by ID and update it
    const index = this.items.findIndex((item) => item.id === updatedItem.id);
    if (index !== -1) {
      this.items[index] = { ...updatedItem };
    }
  }
}

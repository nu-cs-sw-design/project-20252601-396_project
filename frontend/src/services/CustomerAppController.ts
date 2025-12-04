import apiClient from './api';
import * as Types from '../types/index';
import { Payment } from '../types/index';

class CustomerAppController {
  private currentOrderId: number | null = null;

  // Start a new order
  async startOrder(): Promise<Types.Order> {
    try {
      const response = await apiClient.post<Types.ApiResponse<Types.Order>>(`/orders`);
      console.log('Start Order Responseee:', response.data.data);
      if (response.data.data) {
        this.currentOrderId = response.data.data.id;
        return response.data.data;
      }
      
      throw new Error('Failed to create order: No order data returned');
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Failed to create order');
    }
  }

  // Browse menu - Get menu categories
  async browseMenu(): Promise<string[]> {
    try {
      const response = await apiClient.get<Types.ApiResponse<string[]>>('/menu/categories');
      
      if (response.data.data) {
        return response.data.data;
      }
      
      return [];
    } catch (error: any) {
      console.error('Error browsing menu:', error);
      throw new Error(error.response?.data?.message || 'Failed to load menu categories');
    }
  }

  // Get menu items by category
  async getMenuItemsByCategory(category: string): Promise<Types.MenuItem[]> {
    try {
      const response = await apiClient.get<Types.ApiResponse<Types.MenuItem[]>>(
        `/menu/items-by-category/${encodeURIComponent(category)}`
      );
      
      if (response.data.data) {
        return response.data.data;
      }
      
      return [];
    } catch (error: any) {
      console.error('Error getting menu items:', error);
      throw new Error(error.response?.data?.message || 'Failed to load menu items');
    }
  }

  // Get item details
  async getItemDetails(itemID: string): Promise<Types.MenuItem> {
    try {
      const response = await apiClient.get<Types.ApiResponse<Types.MenuItem>>(
        `/menu/items/${itemID}`
      );
      
      if (response.data.data) {
        return response.data.data;
      }
      
      throw new Error('Failed to get item details: No data returned');
    } catch (error: any) {
      console.error('Error getting item details:', error);
      throw new Error(error.response?.data?.message || 'Failed to load item details');
    }
  }

  // Add item to order
  async addItemToOrder(
    orderID: number,
    itemID: string,
    quantity: number,
    customizations: string
  ): Promise<Types.Order> {
    try {
      const response = await apiClient.post<Types.ApiResponse<Types.Order>>(
        `/orders/${orderID}/items`,
        {
          menu_item_id: itemID,
          quantity,
          customizations
        }
      );
      
      if (response.data.data) {
        return response.data.data;
      }
      
      throw new Error('Failed to add item to order: No order data returned');
    } catch (error: any) {
      console.error('Error adding item to order:', error);
      throw new Error(error.response?.data?.message || 'Failed to add item to order');
    }
  }

  // Edit item in order
  async editItemInOrder(
    orderID: number,
    itemID: string,
    quantity: number,
    customizations: string
  ): Promise<Types.Order> {
    try {
      const response = await apiClient.put<Types.ApiResponse<Types.Order>>(
        `/orders/${orderID}/items`,
        {
          menu_item_id: itemID,
          quantity,
          customizations
        }
      );
      
      if (response.data.data) {
        return response.data.data;
      }
      
      throw new Error('Failed to edit item: No order data returned');
    } catch (error: any) {
      console.error('Error editing item:', error);
      throw new Error(error.response?.data?.message || 'Failed to edit item');
    }
  }

  // Remove item from order
  async removeItemFromOrder(orderID: number, itemID: string): Promise<Types.Order> {
    try {
      const response = await apiClient.delete<Types.ApiResponse<Types.Order>>(
        `/orders/${orderID}/items/${itemID}`
      );
      
      if (response.data.data) {
        return response.data.data;
      }
      
      throw new Error('Failed to remove item: No order data returned');
    } catch (error: any) {
      console.error('Error removing item:', error);
      throw new Error(error.response?.data?.message || 'Failed to remove item');
    }
  }

  // Review current order
  async reviewCurrentOrder(orderID: number): Promise<Types.Order> {
    try {
      const response = await apiClient.get<Types.ApiResponse<Types.Order>>(
        `/orders/${orderID}`
      );
      
      if (response.data.data) {
        return response.data.data;
      }
      
      throw new Error('Failed to review order: No order data returned');
    } catch (error: any) {
      console.error('Error reviewing order:', error);
      throw new Error(error.response?.data?.message || 'Failed to load order');
    }
  }

  // Confirm order and select payment option
  async confirmOrder(orderID: number): Promise<Types.Order> {
    try {
        // Mark as pay at counter
        const response = await apiClient.put<Types.ApiResponse<Types.Order>>(
          `/orders/${orderID}/confirm`
        );
        
        if (response.data.data) {
          return response.data.data;
        }
      
      
      throw new Error('Failed to confirm order: No order data returned');
    } catch (error: any) {
      console.error('Error confirming order:', error);
      throw new Error(error.response?.data?.message || 'Failed to confirm order');
    }
  }

  // Pay on system using card
  async payOnSystem(orderID: number, cardInfo: string): Promise<Payment> {
    try {
      const cardInfoString = typeof cardInfo === 'string' 
        ? cardInfo 
        : JSON.stringify(cardInfo);
      
      const response = await apiClient.post<Types.ApiResponse<Payment>>(
        `/payments/process-system`,
        { order_id: orderID, card_info: cardInfoString }
      );
      
      if (response.data.data) {
        return response.data.data;
      }
      
      throw new Error('Failed to process payment: No payment data returned');
    } catch (error: any) {
      console.error('Error processing payment:', error);
      throw new Error(error.response?.data?.message || 'Failed to process payment');
    }
  }

  getCurrentOrderId(): number | null {
    return this.currentOrderId;
  }

  setCurrentOrderId(orderId: number | null): void {
    this.currentOrderId = orderId;
  }

  clearCurrentOrder(): void {
    this.currentOrderId = null;
  }
}

export const customerAppController = new CustomerAppController();
export default CustomerAppController;


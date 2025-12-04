import apiClient from './api';
import * as Types from '../types/index';

class ManagerAppController {
  // List all menu items
  async listMenuItems(): Promise<Types.MenuItem[]> {
    try {
      const response = await apiClient.get<Types.ApiResponse<Types.MenuItem[]>>(
        '/menu/items'
      );
      
      if (response.data.data) {
        return response.data.data;
      }
      
      return [];
    } catch (error: any) {
      console.error('Error listing menu items:', error);
      throw new Error(error.response?.data?.message || 'Failed to load menu items');
    }
  }

  // Add a new menu item
  async addMenuItem(
    name: string,
    price: number,
    category: string,
    description: string
  ): Promise<Types.MenuItem> {
    try {
      const response = await apiClient.post<Types.ApiResponse<Types.MenuItem>>(
        '/menu/items',
        {
          name,
          price,
          category,
          description
        }
      );
      
      if (response.data.data) {
        return response.data.data;
      }
      
      throw new Error('Failed to add menu item: No item data returned');
    } catch (error: any) {
      console.error('Error adding menu item:', error);
      throw new Error(error.response?.data?.message || 'Failed to add menu item');
    }
  }

  // Update an existing menu item
  async updateMenuItem(
    itemID: string,
    price: number,
    description: string
  ): Promise<void> {
    try {
      await apiClient.put<Types.ApiResponse<void>>(
        `/menu/items/${itemID}`,
        {
          price,
          description
        }
      );
    } catch (error: any) {
      console.error('Error updating menu item:', error);
      throw new Error(error.response?.data?.message || 'Failed to update menu item');
    }
  }

  // Show daily sales summary
  async showDailySalesSummary(date: Date | string): Promise<Types.DailySalesSummary> {
    try {
      // Convert date to ISO string format (YYYY-MM-DD)
      const dateString = typeof date === 'string' 
        ? date 
        : date.toISOString().split('T')[0];
      
      const response = await apiClient.get<Types.ApiResponse<Types.DailySalesSummary>>(
        `/reports/sales-summary/${dateString}`
      );
      
      if (response.data.data) {
        return response.data.data;
      }
      
      throw new Error('Failed to generate sales summary: No data returned');
    } catch (error: any) {
      console.error('Error generating daily sales summary:', error);
      throw new Error(error.response?.data?.message || 'Failed to generate sales summary');
    }
  }
}

export const managerAppController = new ManagerAppController();
export default ManagerAppController;

import React from 'react';
import { render, waitFor, screen } from '@testing-library/react';
import UserHome from '../app/repos/page'; // Ensure this path is correct
import fetchMock from 'jest-fetch-mock';

fetchMock.enableMocks();

describe('UserHome Component', () => {
  beforeEach(() => {
    fetch.resetMocks();
  });

  it('renders without crashing and fetches data correctly', async () => {
    fetch.mockResponses(
      [JSON.stringify({ stargazers_count: 123 })],
      [JSON.stringify({ pullRequests: [{ created_at: '2021-01-01', title: 'PR Title', description: 'PR Description' }] })]
    );
  });
});

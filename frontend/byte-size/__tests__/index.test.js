import { render, screen, waitFor } from '@testing-library/react';
import UserHome from '../app/home/page'; // Adjust this path as per your project
import '@testing-library/jest-dom';
import fetchMock from 'jest-fetch-mock';
import { useSession } from "next-auth/react";

fetchMock.enableMocks();

jest.mock('next-auth/react', () => ({
  useSession: jest.fn(),
}));

describe('Test test', () => {
    test('adds 1 + 2 to equal 3', () => {
    expect(1+2).toBe(3);
    });
});

describe('UserHome Tests', () => {
  beforeEach(() => {
    fetch.resetMocks();
  });

  it('loads and displays subscribed repositories', async () => {
    useSession.mockReturnValue({ data: { token: 'fake-token' }, status: 'authenticated' });
    const mockSubscribedRepos = [{ name: 'subscribed-repo1', url: 'http://subscribed-repo1.com' }];
    fetch.mockResponses(
      [JSON.stringify(mockSubscribedRepos), { status: 200 }],
      [JSON.stringify([]), { status: 200 }] // Mock response for getAllRepos
    );

    render(<UserHome />);
    await waitFor(() => {
      expect(screen.getByText('subscribed-repo1')).toBeInTheDocument();
    });
  });

  it('loads and displays all repositories', async () => {
    useSession.mockReturnValue({ data: { token: 'fake-token' }, status: 'authenticated' });
    const mockRepos = [{ name: 'repo1', url: 'http://repo1.com' }];
    fetch.mockResponses(
      [JSON.stringify([]), { status: 200 }], // Mock response for getSubbedRepos
      [JSON.stringify(mockRepos), { status: 200 }]
    );

    render(<UserHome />);
    await waitFor(() => {
      expect(screen.getByText('repo1')).toBeInTheDocument();
    });
  });
});
